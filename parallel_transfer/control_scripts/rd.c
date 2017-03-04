/*
 Recursive, multi-threaded directory tree read.
*/

#define HAVE_D_TYPE     /* Remove for kernels < 2.6.4 */
#define _GNU_SOURCE
#include <dirent.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/syscall.h>
// #include <gnutls/gnutls.h>
#include <pthread.h>
#define NUM_THREADS    12

long long d_to_proc=0;
int tCount=0;
char *outDir="/tmp";

struct linux_dirent {
 long           d_ino;
 off_t          d_off;
 unsigned short d_reclen;
 char           d_name[];
};

struct qEnt { 
 char    *dName;
 struct  qEnt* next;
};

struct qEnt* head = NULL;
struct qEnt* tail = NULL;

pthread_mutex_t lock_pp;  /* Push and pop lock */

char *qPop(){
 struct qEnt* t = head;
 char *rVal;
 if ( head==NULL ) {
  return NULL;
 }
 if ( head==tail ){
  rVal=strdup(t->dName);
  head=tail=NULL;
 } else {
  rVal=strdup(t->dName);
  head=head->next;
 }
 free(t->dName);
 free(t);
 return(rVal);
}

qPush( char *s ) {
 struct qEnt* t = (struct qEnt*)malloc(sizeof(struct qEnt));
 t->dName=strdup(s);
 if ( t->dName == NULL ) {
  printf("Out of memory\n");
  exit(-1);
 }
 t->next=NULL;
 if ( head==NULL &&  tail==NULL ) {
  head=tail=t;
  return;
 }
 tail->next=t;
 tail=t;
}

void *rdirect(void *threadId){
 int myTid;
 int fd;
 int nread;
 int BUF_SIZE=10*1024*1024;
 char *buf=(char *)malloc(BUF_SIZE);  /* Buffer for reading directory */
 char *dN;
 char myOFile[1024];
 FILE *oFile;

 pthread_mutex_lock(&lock_pp);
  myTid=tCount;
  ++tCount;
  sprintf(myOFile,"%s/cnh_rd_%5.5d.txt",outDir,myTid);
 pthread_mutex_unlock(&lock_pp);
 oFile=fopen(myOFile,"w");
 if ( oFile == NULL ) {
  return;
 }

 /* Queue pop handler                                  */
 while(1){
 dN=NULL;
 while ( dN == NULL && d_to_proc > 0 ) {
 /* Read the directory, taking name from next in queue */
 /* BEGIN mutex */
 pthread_mutex_lock(&lock_pp);
 dN = qPop();
 pthread_mutex_unlock(&lock_pp);
 /* END mutex   */
 }

 /* Return/wait if nothing queued */
 if ( dN==NULL ) {
  return;
 }
 /* Open                          */
 /* printf("Opening %s\n",dN);    */
 fd = open(dN , O_RDONLY | O_DIRECTORY);
 if (fd == -1) { return; }

 for ( ; ; ) {
  nread = syscall(SYS_getdents, fd, buf, BUF_SIZE);
  if (nread == -1)
   return;
  if (nread == 0)
   break;
  struct linux_dirent *d;
  char d_type;
  int bpos;
  for (bpos = 0; bpos < nread;) {
   d = (struct linux_dirent *) (buf + bpos);
   d_type = *(buf + bpos + d->d_reclen - 1);
   if ( strcmp(d->d_name,".")   != 0 &&
        strcmp(d->d_name,".." ) != 0  ) {
    fprintf(oFile,"%-2s  ", (d_type == DT_REG) ?  "r" :
                     (d_type == DT_DIR) ?  "d" :
                     (d_type == DT_FIFO) ? "o" :
                     (d_type == DT_SOCK) ? "o" :
                     (d_type == DT_LNK) ?  "l" :
                     (d_type == DT_BLK) ?  "o" :
                     (d_type == DT_CHR) ?  "o" : "o");
    fprintf(oFile,"%s/%s%c %d\n",dN,d->d_name,(char)0,myTid);
   }


   /* Read entries                  */
   /*  not directory                */
   /*   uuencode path               */
   /*   write                       */
   /*  directory                    */
   /*   push to queue               */
   if ( d_type                 == DT_DIR && 
        strcmp(d->d_name,".")  != 0      && 
        strcmp(d->d_name,"..") != 0 ) {
    char *dNext=(char *)malloc(strlen(dN)+1+strlen(d->d_name)+1);
    sprintf(dNext,"%s/%s",dN,d->d_name);
    /* BEGIN mutex */
    pthread_mutex_lock(&lock_pp);
    qPush(dNext);
    ++d_to_proc;
    pthread_mutex_unlock(&lock_pp);
    /* END mutex   */

    /* rdirect();  */
    free(dNext);
   }
   bpos += d->d_reclen;
  }
 }
 /* printf("Closing %s\n",dN); */
 close(fd);
 free(dN);
 pthread_mutex_lock(&lock_pp);
 --d_to_proc;
 pthread_mutex_unlock(&lock_pp);
 /* Call rdirect recursively      */
 }
}

main(int argc, char *argv[]){
 int rc;
 long th;
 pthread_t threads[NUM_THREADS];
 char *dNext;

 if ( argc != 2 ) {
  printf("Usage \"%s root_directory\"\n",argv[0]);
  exit(-1);
 }
 dNext=(char *)malloc(strlen(argv[1]+1));
 sprintf(dNext,"%s",argv[1]);
 qPush( argv[1] );
 ++d_to_proc;
 free(dNext);


 if ( pthread_mutex_init(&lock_pp, NULL) != 0 ) {
  printf("Usage \"Lock failed\"\n");
  exit(-1);
 }
 for(th=0;th<NUM_THREADS;th++){
  printf("In main: creating thread %ld\n", th);
  rc = pthread_create(&threads[th], NULL, rdirect, (void *)th);
  if (rc){
   printf("ERROR; return code from pthread_create() is %d\n", rc);
   exit(-1);
  }
 }

 /* Last thing that main() should do */
 pthread_exit(NULL);

 /* rdirect(); */
}
