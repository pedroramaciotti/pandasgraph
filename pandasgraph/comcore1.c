/*
gcc comcore1.c -O9 -o comcore1

./comcore1 k com.txt pairs.txt
- com.txt contains the list of all communities.  
One community on each line:  
i0 i1 i2 ... in  
where:  
i0 i1 i2 ... in is the list of the nodes in the community.
- pair.txt contains the list of all pairs of nodes appearing in more that k times in a same community: "node1 node2 times" on each line.
*/

#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdbool.h>
//#include <math.h>
//#include <omp.h>

#define NLINKS 200000000 //Maximum number of links, will automatically increase if needed.
#define NNODES 100000000 //Maximum number of nodes, will automatically increase if needed.

//bipartite graph structure
typedef struct {
	unsigned nb;//number of bottom nodes
	unsigned nt;//number of top nodes
	unsigned e;//number of edges

	unsigned *db; //bottom degrees
	unsigned *cdb; //cumulative bottom degrees: (start with 0) length=nb+1
	unsigned *adjb; //list of neighbors of bottom nodes
	unsigned *dt; //top degrees
	unsigned *cdt; //cumulative top degrees: (start with 0) length=bt+1
	unsigned *adjt; //list of neighbors of top nodes
} bigraph;

//used in qsort
int cmpfunc(void const *a, void const *b){
	unsigned const *pa = a;
	unsigned const *pb = b;
	if (*pa<*pb)
		return -1;
	return 1;
}

//reading communities from file to make the bipartite graph
bigraph* readcoms(char* communities){
	unsigned e1=NLINKS,n1=NNODES,u,v,i,max;
	char c;
	bigraph *g=malloc(sizeof(bigraph));
	FILE *file;

	g->nb=0;
	g->nt=0;
	g->e=0;
	g->dt=calloc(n1,sizeof(unsigned));
	g->adjt=malloc(e1*sizeof(unsigned));

	file=fopen(communities,"r");
	while(fscanf(file,"%u%c",&u,&c)==2){
		g->adjt[g->e]=u;
		g->dt[g->nt]++;
		if (++g->e==e1) {
			//printf("increasing maximum number of edges\n");
			e1+=NLINKS;
			g->adjt=realloc(g->adjt,e1*sizeof(unsigned));
		}
		g->nb=(g->nb>u+1)?g->nb:u+1;
		if (c=='\n') {
			if (++g->nt==n1) {
				//printf("increasing maximum number of nodes\n");
				g->dt=realloc(g->dt,(n1+NNODES)*sizeof(unsigned));
				bzero(g->dt+n1,NNODES*sizeof(unsigned));
				n1+=NNODES;
			}
		}
	}
	fclose(file);
	g->adjt=realloc(g->adjt,g->e*sizeof(unsigned));
	g->dt=realloc(g->dt,g->nt*sizeof(unsigned));

	g->cdt=malloc((g->nt+1)*sizeof(unsigned));
	g->cdt[0]=0;
	max=0;
	for (u=0;u<g->nt;u++){
		g->cdt[u+1]=g->cdt[u]+g->dt[u];
		max=(g->dt[u]>max)?g->dt[u]:max;
	}
	printf("Maximum top degree: %u\n",max);

	g->db=calloc(g->nb,sizeof(unsigned));
	for (i=0;i<g->e;i++){
		g->db[g->adjt[i]]++;
	}

	g->cdb=malloc((g->nb+1)*sizeof(unsigned));
	g->cdb[0]=0;
	max=0;
	for (i=0;i<g->nb;i++){
		g->cdb[i+1]=g->cdb[i]+g->db[i];
		max=(g->db[i]>max)?g->db[i]:max;
	}
	printf("Maximum bot degree: %u\n",max);

	g->adjb=malloc(g->e*sizeof(unsigned));
	bzero(g->db,g->nb*sizeof(unsigned));
	for (u=0;u<g->nt;u++){
		for (i=g->cdt[u];i<g->cdt[u+1];i++) {
			v=g->adjt[i];
			g->adjb[g->cdb[v]+g->db[v]++]=u;
			//printf("%u %u\n",u,v);
		}
	}

	//Sorting bottom nodes to save time later...
	for (u=0;u<g->nb;u++){
		qsort(g->adjb+g->cdb[u],g->db[u],sizeof(unsigned),cmpfunc);
	}

	return g;
}

void freebigraph(bigraph *g){
	free(g->db);
	free(g->cdb);
	free(g->adjb);
	free(g->dt);
	free(g->cdt);
	free(g->adjt);
	free(g);
}

//print all pairs of nodes in more than k communities
void pairs(bigraph *g, unsigned k, char* output){
	unsigned i,j,u,v,w,n;
	bool *tab;
	unsigned *list,*inter;
	FILE* file=fopen(output,"w");

	tab=calloc(g->nb,sizeof(bool));
	list=malloc(g->nb*sizeof(unsigned));
	inter=calloc(g->nb,sizeof(unsigned));

	for (u=0;u<g->nb;u++){//embarrassingly parallel...
		n=0;
		for (i=g->cdb[u];i<g->cdb[u+1];i++){
			v=g->adjb[i];
			for (j=g->cdt[v];j<g->cdt[v+1];j++){
				w=g->adjt[j];
				if (w==u){//make sure that (u,w) is processed only once (out-neighbors of u are sorted)
					break;
				}
				if(tab[w]==0){
					list[n++]=w;
					tab[w]=1;
				}
				inter[w]++;
				//printf("%u %u %le\n",u,w,val);//to print the pairs and similarity
			}
		}
		for (i=0;i<n;i++){
			w=list[i];
			if (inter[w]>=k){
				fprintf(file,"%u %u %u\n",u,w,inter[w]);
			}
			tab[w]=0;
			inter[w]=0;
		}
	}

	free(tab);
	free(list);
	free(inter);

	fclose(file);
}

int main(int argc,char** argv){
	bigraph* g;
	unsigned i,k;

	time_t t0,t1,t2;
	t1=time(NULL);
	t0=t1;

	printf("Reading comminities from file %s\n",argv[2]);
	g=readcoms(argv[2]);

	t2=time(NULL);
	printf("- Time = %ldh%ldm%lds\n",(t2-t1)/3600,((t2-t1)%3600)/60,((t2-t1)%60));
	t1=t2;

	printf("Number of top nodes (communities): %u\n",g->nt);
	printf("Number of bottom nodes (nodes): %u\n",g->nb);
	printf("Number of edges: %u\n",g->e);

	t2=time(NULL);
	printf("- Time = %ldh%ldm%lds\n",(t2-t1)/3600,((t2-t1)%3600)/60,((t2-t1)%60));
	t1=t2;

	printf("finding pairs of nodes in more than %s communities\n",argv[1]);
	k=atoi(argv[1]);
	printf("printing them in file %s\n",argv[3]);
	pairs(g,k,argv[3]);

	t2=time(NULL);
	printf("- Time = %ldh%ldm%lds\n",(t2-t1)/3600,((t2-t1)%3600)/60,((t2-t1)%60));
	t1=t2;

	freebigraph(g);

	return 0;
}

