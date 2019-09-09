/*LUANA BALADOR BELISÁRIO*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define BUFFER_SIZE 5192



typedef struct Dictio{
	char word[100];
}Dictio;

char* convert_lower(char * expression);
int binary_search(Dictio* v, char* chave, int beg, int end);
void mergesort (Dictio* v, int beg, int end);
Dictio* create_Dictio(FILE* in, int* n);
void classifying(Dictio* dic_pos, Dictio* dic_neg, FILE* read, FILE* class, int positive_size, int negative_size, int flag);


int main(int argc, char const *argv[])
{
	Dictio *dic_pos, *dic_neg;
	int positive_size, negative_size, flag = 0;
	
	char positive[100];
	char negative[100];
	char reading[100];

	printf("Digite o nome completo do arquivo contendo o léxico de palavras/expressões positivas (exemplo: 'positivos.txt')\n");
	scanf("%s", positive);
	printf("Digite o nome completo do arquivo contendo o léxico de palavras/expressões negativas (exemplo: 'negativos.txt')\n");
	scanf("%s", negative);
	printf("Digite o nome completo do arquivo de leitura (exemplo: 'leitura.txt')\n");
	scanf("%s", reading);

	FILE *pos = fopen(positive, "r");
	FILE *neg = fopen(negative, "r");
	FILE *read = fopen(reading, "r");
	FILE *class = fopen("resultado.txt", "w");

	

	dic_pos = create_Dictio(pos, &positive_size);
	dic_neg = create_Dictio(neg, &negative_size);
	mergesort(dic_pos, 0, positive_size-1);
	mergesort(dic_neg, 0, negative_size-1);

	classifying(dic_pos, dic_neg, read, class, positive_size, negative_size, flag);

	free(dic_pos);
	free(dic_neg);
	fclose(pos);
	fclose(neg);
	fclose(read);
	fclose(class);

	
	return 0;
}


char* convert_lower(char * expression){
    for(int i = 0; expression[i] != '\0'; i++){
        expression[i] = tolower(expression[i]);
    }
    
    return expression;
}

int binary_search(Dictio* v, char* chave, int beg, int end) {
	if (beg > end) return 0;
	
	int center = (int)((beg+end)/2.0);
	if (strcmp(v[center].word, chave) == 0){
		return 1;
	}

	if (strcmp(chave, v[center].word) < 0)
		return binary_search(v, chave, beg, center-1);

	else 
		return binary_search(v, chave, center+1, end);
}

void mergesort (Dictio* v, int beg, int end) {
	if (end <= beg) return;

	int center = (int)((end+beg)/2.0);

	mergesort(v, beg, center);
	mergesort(v, center+1, end);

	Dictio* aux = (Dictio*) malloc(sizeof(Dictio) * (end-beg+1) );
	
	int i = beg;	
	int j = center+1;
 	int k = 0;	

	while (i <= center && j <= end) {
		if (strcmp(v[i].word, v[j].word) <= 0) {
			strcpy(aux[k].word, v[i].word);
			i++;
		} 
		else {
			strcpy(aux[k].word, v[j].word);
			j++; 
		}
		k++; 
	}

	while (i <= center) {
		strcpy(aux[k].word, v[i].word);
		i++; k++;
	}
	while (j <= end) {
		strcpy(aux[k].word, v[j].word);
		j++; k++;
	}	
	for (i = beg, k = 0; i <= end; i++, k++) {
		strcpy(v[i].word, aux[k].word);
	}

	free(aux); 
}

Dictio* create_Dictio(FILE* in, int* n){
	Dictio* v = (Dictio*)malloc(BUFFER_SIZE * sizeof(Dictio));
	int i = 0;
	char aux[46];

	while(!feof(in)) {
	fgets(aux, 46, in);
	aux[strlen(aux) - 1] = '\0';
	/*strcpy(aux, */convert_lower(aux);
	if(strcmp(aux, "\0")){
		strcpy(v[i].word, aux);
		i++;
	}
	if (i % BUFFER_SIZE == 0)
		v = realloc(v, (i + BUFFER_SIZE) * sizeof(Dictio));
	}
	*n = i;
	v = realloc(v, *n * sizeof(Dictio));
	return v;
}

void classifying(Dictio* dic_pos, Dictio* dic_neg, FILE* read, FILE* class, int positive_size, int negative_size, int flag){
	char expression[100];
	char ans[100];
	char c;
	int posit = 0, negat = 0;
	while(!feof(read)){
		while(!feof(read) && !fscanf(read, "%[^ \n,;.'_\"()]", expression)){
			c = fgetc(read);
			if(c == '\n' || feof(read)){
				if(posit-negat == 0)
					fprintf(class, "0\n");
				else if(posit-negat > 0)
					fprintf(class, "1\n");
				else
					fprintf(class, "-1\n");
				posit = negat = flag = 0;
			}
			strcpy(expression, "\0");
		}

		
		strcpy(ans, expression);
		if (binary_search(dic_pos, convert_lower(ans), 0, positive_size-1))
		{
			posit++;
		}
		else if(binary_search(dic_neg, convert_lower(ans), 0, negative_size-1))
		{
			negat++;
		}
	}
	
}
