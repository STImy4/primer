#include <stdio.h>
#include <stdlib.h>
#include <string.h> //библиотека с работой со строками
#include <time.h> // библиотека для работы с временем

#define ESIZE 20 // макс кол-во событий
#define UNIX_TM 1 // 1=отображать время в unix формате
#define EVENTS_FILE "events.txt" //объявление файла с названием events.txt

typedef struct dateTime { // тип данных даты и времени
    int d,m,y,h,mn; 
} dt;

dt setDT (int d, int m, int y, int h, int mn) {
    dt d1; 
    d1.d=d;
    d1.m=m,
    d1.y=y;
    d1.h=h;
    d1.mn=mn;
    return d1;
};

int checkdt(int dd, int dm, int dy, int dh, int dmn) { //проверка существования даты
    int vis_year, month, tru;
    
    vis_year=0; 
    month=0;
    tru=1;
    
    if(dy%4==0) vis_year = 1;
        
    if(dm==2) month = 1;
    else if((dm>0) && (dm<8) && (dm%2==1)) month = 2;
        else if((dm>7) && (dm<13) && (dm%2==0)) month = 2;
       
    if(month==1)  {
        if(vis_year==1) {
                if((dd<1)||(dd>29)) tru=0;
            }
            else if (vis_year==0) {
                if((dd<1)||(dd>28)) tru=0;
            }
        }
    else if(month==2) {
        if((dd<1)||(dd>31)) tru=0;
    }
    else {
        if((dd<1)||(dd>30)) tru=0;
    }
    if((dmn<0)||(dmn>59)||(dh<0)||(dh>23)||(dm<1)||(dm>12)||(dy<1900)||(dy>2100)) return 0 ;
    else return tru ;
}

typedef struct event { //структура события
    int num;  //уникальный номер
    int type; //тип
    dt date;  //дата числами
    long int tms;  //дата в формате unix
    char person[50]; // ФИО
    char info[100];  // Инфо
} event;

event setEvent (int num, int type, dt d1, char *sP, char *sI) { //заполнение события
    event e1;
    e1.num = num;
    e1.type = type;
    e1.date.d = d1.d;
    e1.date.m = d1.m;
    e1.date.y = d1.y;
    e1.date.h = d1.h;
    e1.date.mn = d1.mn;
    
    struct tm vt;

	vt.tm_mday = d1.d;
	vt.tm_mon = d1.m-1; // месяц начинается с 0
	vt.tm_year = d1.y-1900; //год начинается с 1970
	vt.tm_hour = d1.h;
	vt.tm_min = d1.mn;
	vt.tm_sec = 0;
	vt.tm_isdst = 0;
    e1.tms = mktime(&vt);
    
    strcpy(e1.person,sP);
    strcpy(e1.info,sI);
    return e1;
}

event emptyEvent () {
    event e1; //результат события
    dt d1;
    d1=setDT(1,1,1970,0,0);
    char sempty[]="-";
    e1=setEvent(-1, 0, d1, sempty, sempty);
}

event fillEvent (int n) { //сгенерированные события
    dt dd;
    event e1;
    char *sP, *sI;
    if (n==1) {
        dd = setDT (1, 8, 2023, 18, 0);
        sP = "Иванов Петр Сергеевич";
        sI = "Встречаемся на Красной площади";
        e1 = setEvent (1, 1, dd, sP, sI);
    }
    else if (n==2) {
        dd = setDT (5, 05, 2020, 17, 30);
        sP = "Петров Сергей Иванович";
        sI = "Встречаемся в кафе \"Шоколадница\"";
        e1 = setEvent (2, 1, dd, sP, sI);
    }
    else {
        dd = setDT (2, 10, 2022, 12, 15);
        sP = "Сергеев Иван Петрович";
        sI = "Зайти в гости в день рождения";
        e1 = setEvent (3, 2, dd, sP, sI);
    }
    return e1;
}

void printN (int t, char *s) { //печать числа, вывод числа с 0, если оно из 1 цифроы
    if (t <10) {
        printf ("0%d%s", t, s);
    } else {
        printf ("%d%s", t, s);
    }
}

void printEvent (event e1, int nstr) { // вывод события на консоль
    int len = 100; // длина строки оформления
    int printTms = UNIX_TM; // вывод unix формата времени
    if (nstr==1) {
        for (int i=1; i<=len; i++) printf ("-");
        printf ("\n");
    }
    if (e1.num<10) printf("N %d  ",e1.num);
    else if (e1.num<100) printf("N %d ",e1.num);
    else printf("N %d",e1.num);
    
    if (((e1.type==1)||(e1.type==2))&&((e1.num>0)&&(e1.num<=ESIZE))) { //проверяем корректность данных в событии
        if (e1.type==1) printf("Встреча       |");
        if (e1.type==2) printf("День рождения |");
        
        printf (" Дата и время | ");
        printN (e1.date.d, ".");
        printN (e1.date.m, ".");
        printf ("%d ",e1.date.y);
        printN (e1.date.h, ":");
        printN (e1.date.mn, " ");
        if (printTms==1) printf ("(unix формат: %ld)", e1.tms);
        printf ("\n");
        printf ("                   |          ФИО | %s\n", e1.person);
        printf ("                   |         Инфо | %s\n", e1.info);
    }
    else {
        printf ("Данные о событии отсутствуют или ошибочные\n");
    }
    for (int i=1; i<=len; i++) printf ("-");
    printf ("\n");
}

dt getDate() { //ввод даты, с возможностью повторного ввода, если ошибка
    int checkS=0, checkD = 0;
    char res[]="n";
    dt ddate;
    int dd,dm,dy,dh,dmn;
    ddate = setDT (0, 0, 0, 0, 0);
    do {
        printf ("Введите дату в формате день/месяц/год/час/минуты (пример: 1/1/1970/9/30): ");
        checkD = 0;
        checkS = 0;
        
        if (scanf("%d%*c%d%*c%d%*c%d%*c%d",&dd, &dm, &dy, &dh, &dmn)==5) {
            checkS = checkdt(dd, dm, dy, dh, dmn);
        }
        while ((getchar()) != '\n');//очищение потока ввода
        if (checkS==1) { 
            ddate = setDT (dd, dm, dy, dh, dmn);
            checkD = 1;
        }
        else {
            printf("Некорректное значение даты. Хотите повторить ввод? нажмите \"y\" если да: ");
            scanf("%1s",res);
            while ((getchar()) != '\n');//очищение потока ввода
        }
   } while ((strcmp(res,"y")==0) && (checkD==0));
   return ddate;
}

long int getDateInt() { //ввод даты и перевод в кол-во секунд
    dt d1;
    struct tm vt;
    long int res=0;
    
    d1 = getDate();
    if (d1.d!=0) {
        vt.tm_mday = d1.d;
	    vt.tm_mon = d1.m-1;
	    vt.tm_year = d1.y-1900;
	    vt.tm_hour = d1.h;
	    vt.tm_min = d1.mn;
	    vt.tm_sec = 0;
	    vt.tm_isdst = 0;
        res = mktime(&vt);
    }
    return res;
}

event getEvent(int num) { //ввод события
    event i_event;
    float t=0;
    dt ddate;

    char sP[50];
    char sInfo[100];
    char res[]="n";
    
    do {
        printf ("Тип события (1 - встреча, 2 - день рождения): ");
        if ((scanf("%f",&t)==1) && (t==1 || t==2)) { 
            int t; 
            while ((getchar()) != '\n');//очищение потока ввода после scanf 
        }
        else {
            while ((getchar()) != '\n');//очищение потока ввода
            printf("Некорректное значение. Хотите повторить ввод? нажмите \"y\" если да: ");
            scanf("%s",res);
            while ((getchar()) != '\n');//очищение потока ввода
        }
    } while ((strcmp(res,"y")==0) && !(t==1 || t==2));
       
    if (t!=1 && t!=2) {
        printf ("Тип указан не верно, команда отменена\n");
        i_event = emptyEvent();
        return i_event;
    }
   
    printf ("Дата события. ");
    ddate = getDate();
    if (ddate.d==0) {
        printf ("Дата события указана не верно, команда отменена\n");
        i_event = emptyEvent();
        return i_event;
    }   
   
    printf ("ФИО: ");
    fgets(sP,50,stdin); 

    // функция fgets перенос строки записывает в строку, нужно его заменить на /0
    char *lbr;  //переменная для сохранения указателя на перенос строки
    lbr = strchr(sP,10); // поиск первого вхождения переноса строки
    if (lbr!=NULL) { *lbr = 0; } //замена на 0
    
    printf ("Инфо: ");
    fgets(sInfo,100,stdin); 
    
    lbr = strchr(sInfo,10);
    if (lbr!=NULL) { *lbr = 0; }
    
    i_event = setEvent (num, t, ddate, sP, sInfo);
    return i_event;
}

event modEvent(event e1) { //выборочное редактирование события 
    event i_event;
    float t=0;
    dt ddate;
    
    char sP[50];
    char sInfo[100];

    char res[]="n";
    char eres[]="n";
    
    printf ("Вы выбрали для редактирования событие:\n");
    printEvent(e1,1);
    
    t = e1.type;
    printf ("Хотите изменить тип события? нажмите \"y\" если да:\n");
    if ((scanf("%s",eres)==1) && (strcmp(eres,"y")==0)) {
        do {
            printf ("Тип события (1 - встреча, 2 - день рождения): ");
            if ((scanf("%f",&t)==1) && (t==1 || t==2)) { 
                int t; 
            }
            else {
                while ((getchar()) != '\n');//очищение потока ввода
                printf("Некорректное значение типа. Хотите повторить ввод? нажмите \"y\" если да: ");
                scanf("%s",res);
            }
        } while ((strcmp(res,"y")==0) && !(t==1 || t==2));
    }
    
    while ((getchar()) != '\n');//очищение потока ввода
    strcpy(res,"n");
    strcpy(eres,"n");
    
    ddate = e1.date;
    printf ("Хотите изменить дату события? нажмите \"y\" если да:\n");
    if ((scanf("%s",eres)==1) && (strcmp(eres,"y")==0)) {
        ddate = getDate();
        if (ddate.d==0) ddate = e1.date;
    }
    char *lbr;
    strcpy(sP,e1.person);
    printf ("Хотите изменить ФИО? нажмите \"y\" если да:\n");
    if ((scanf("%s",eres)==1) && (strcmp(eres,"y")==0)) {
        while ((getchar()) != '\n'); // очищение потока ввода
        printf ("ФИО: ");
        fgets(sP,50,stdin); 
        lbr = strchr(sP,10); // поиск первого вхождения переноса строки
        if (lbr!=NULL) { *lbr = 0; } //замена на 0
    }
    
    strcpy(sInfo,e1.info);
    printf ("Хотите изменить Инфо? нажмите \"y\" если да:\n");
    if ((scanf("%s",eres)==1) && (strcmp(eres,"y")==0)) {
        while ((getchar()) != '\n'); // очищение потока ввода
        printf ("Инфо: ");
        fgets(sInfo,100,stdin); 
        lbr = strchr(sInfo,10);
        if (lbr!=NULL) { *lbr = 0; }
    }
    while ((getchar()) != '\n'); // очищение потока ввода
    
    i_event = setEvent (e1.num, t, ddate, sP, sInfo);
    return i_event;
}

int strstrEvent (event e1, char *str) { //проверка вхождения слова в 2 полях события
    int res = 0;
    
    if (strstr (e1.person, str)!=NULL) res = 1;
    else if (strstr (e1.info, str)!=NULL) res = 1;
    
    return res;
}

int getNum (event* em, int n) { // найти значение не использованное в массиве
    int num=1; // начальное значение
    int i=0; //счетчик
    while (i<n) {
        if (em[i++].num == num) {
            num++;
            i=0;
        } 
    }
    return num;
}

void sortEvents (event* em, int n) { //сортировка массива событий по возрастанию
    event et; //переменная для перестановки элементов массива
    int i=0; //счетчик
    while (i<n-1) {
        if (em[i].tms > em[i+1].tms) {
            et=em[i];
            em[i]=em[i+1];
            em[i+1]=et;
            i=0;
        } else { i++; }
    }
}

int choiceMenu () { //вывод меню и возврат выбранной команды
    int len = 100,res=0; //длина строки оформления и результат по умолчанию
    char cmd[10]; // строка для ввода

    printf("Меню для еженедельника, введите одну из следующих команд: \n");
    for (int i=1; i<=len; i++) printf ("-");
    printf ("\n");
    
    printf("view - посмотреть ближайшие события   | new - добавить событие           \n");
    printf("period - посмотреть события за период | edit - редактировать событие     \n");
    printf("search - поиск события                | del - удалить событие            \n");
    printf("out - сохранить в файл все события    | in - загрузить события из файла  \n");
    
    for (int i=1; i<=len; i++) printf ("-");
    printf ("\n");
    
    if (scanf("%10s",cmd)==1) { // меню с выбором команды для еженедельника для пользователя
        if ((strcmp(cmd,"view")==0)) res=1;
        if ((strcmp(cmd,"period")==0)) res=2;
        if ((strcmp(cmd,"search")==0)) res=3;
        if ((strcmp(cmd,"out")==0)) res=4;
        if ((strcmp(cmd,"new")==0)) res=5;
        if ((strcmp(cmd,"edit")==0)) res=6;
        if ((strcmp(cmd,"del")==0)) res=7;
        if ((strcmp(cmd,"in")==0)) res=8;
    }
    while ((getchar()) != '\n');//очищение потока ввода
    return res;
}

void viewEvents (event* em, int n) { //команда просмотра ближайших событий
    event et[ESIZE]; //временный массив для вывода событий
    int cnt=1, ii=0, curtm; //кол-во событий для отображения, счечтки для временного массива, текущее время
    curtm = time(NULL);
    
    printf("Какое количество событий отобразить?  ");
    if (scanf("%d",&cnt)!=1) {
        printf ("Ошибка ввода числа, будет отображено 1 событие\n");
    }
    while ((getchar()) != '\n');//очищение потока ввода
    
    for (int i=0;i<n;i++) {
        if (em[i].tms>=curtm) et[ii++]=em[i];
    }
    if (ii==0) { // нет событий для вывода
        printf ("Результат: события отсутствуют\n\n");    
    } else {
        sortEvents(et,ii); //сортировка по возрастанию даты
        if (cnt>ii) cnt=ii; // выбираем меньшее значение для цикла вывода событий
        for (int i=0;i<cnt;i++) printEvent(et[i],i+1); 
    }
}

void periodEvents(event* em, int n) { //для команды в меню - вывод событий из периода
    event et[ESIZE]; //временный массив для вывода событий
    int ii=0;
    long int p1=0,p2=0;
    printf("Дата начала периода. ");
    p1 = getDateInt();
    if (p1==0) {
        printf("Ошибка указания даты, по умолчанию будет использована текущая дата\n");
        p1== time(NULL);
    }
    printf("Дата окончания периода. ");
    p2 = getDateInt();
    
    if (p1>p2) {
        printf("Ошибка указания даты, по умолчанию будет показано за 30 дней с даты начала периода\n");
        p2=p1+30*24*60*60;
    } 
    
    for (int i=0;i<n;i++){
        if ((em[i].tms>=p1)&&(em[i].tms<=p2)) et[ii++]=em[i];
    }
    
    if (ii==0) { // нет событий для вывода
        printf ("Результат: события в периоде отсутствуют\n\n");    
    } else {
        sortEvents(et,ii); //сортировка по возрастанию даты
        for (int i=0;i<ii;i++) printEvent(et[i],i+1); 
    }
}

void searchEvents (event* em, int n) { //для команды в меню - вывод событий из периода
    event et[ESIZE]; //временный массив для вывода событий
    int ii=0;
    char ss [10];
    printf("Введите слово для поиска в событиях, до 10 символов без пробелов: ");
    
    if (scanf("%10s",ss)!=1) {
        printf ("Ошибка ввода строки, поиск не может быть выполнен.\n");
    } else {
        for (int i=0;i<n;i++){
            if (strstrEvent (em[i], ss)==1) et[ii++]=em[i];
        }
        if (ii==0) { // нет событий для вывода
            printf ("Результат поиска: события отсутствуют\n\n");    
        } else {
            sortEvents(et,ii); //сортировка по возрастанию даты
            for (int i=0;i<ii;i++) printEvent(et[i],i+1); 
        }
    }
    while ((getchar()) != '\n');//очищение потока ввода
}

int editEvent (event* em, int n) { //команда редактирования, возвращает индекс измененного события
    int i, ii=-1, num=0;
    char res[]="n";
    do {
        printf ("Введите номер события для изменения: ");
        if (scanf("%d",&num)==1) {
            i=0;
            while (i<n) {
                if (em[i++].num==num) {
                    ii=i-1;
                    i=n;
                }
            }
            while ((getchar()) != '\n');//очищение потока ввода
            if (ii==-1) {
                printf("Событие с таким номером не найдено. Хотите повторить ввод? нажмите \"y\" если да: ");
                scanf("%s",res);
                while ((getchar()) != '\n');//очищение потока ввода
            }
        } else {
            while ((getchar()) != '\n');//очищение потока ввода
            printf("Ошибка ввода. Хотите повторить ввод? нажмите \"y\" если да: ");
            scanf("%s",res);
            while ((getchar()) != '\n');//очищение потока ввода
        }
    } while ((strcmp(res,"y")==0)&&(ii==-1));
    if (ii==-1) {
        printf("Команда отменена\n\n");
    } else {
        em[ii] = modEvent(em[ii]);
    }
    return ii;
}

int delEvent (event* em, int n) { //команда удаления события, возвращает индекс события, если успешно, и -1 если нет
    int i, ii=-1, num=0;
    char res[]="n";
    do {
        printf ("Введите номер события для удаления: ");
        if (scanf("%d",&num)==1) {
            i=0;
            while (i<n) {
                if (em[i++].num==num) {
                    ii=i-1;
                    i=n;
                }
            }
            while ((getchar()) != '\n');//очищение потока ввода
            if (ii==-1) {
                printf("Событие с таким номером не найдено. Хотите повторить ввод? нажмите \"y\" если да: ");
                scanf("%s",res);
                while ((getchar()) != '\n');//очищение потока ввода
            }
        } else {
            while ((getchar()) != '\n');//очищение потока ввода
            printf("Ошибка ввода. Хотите повторить ввод? нажмите \"y\" если да: ");
            scanf("%s",res);
            while ((getchar()) != '\n');//очищение потока ввода
        }
    } while ((strcmp(res,"y")==0)&&(ii==-1));
    if (ii==-1) {
        printf("Команда отменена\n\n");
    } else {
        em[ii] = em[n-1];
        em[n-1]=emptyEvent();
    }
    return ii;
}

int outEvents (event* em, int n) { //выгрузить в файл, 1 если успешно, 0 если случились ошибки
    FILE *fl;
    fl = fopen(EVENTS_FILE, "w");
    if (fl == NULL) {
        printf("Ошибка открытия файла\n");
        return 0;
    } 
    for (int i=0;i<n;i++) {
        fprintf (fl,"-item:%d\n",i);
        fprintf (fl,"t:%d\n",em[i].type);   
        fprintf (fl,"d:%d.%d.%d %d:%d\n",em[i].date.d,em[i].date.m,em[i].date.y,em[i].date.h,em[i].date.mn);
        fprintf (fl,"p:%s\n",em[i].person);
        fprintf (fl,"i:%s\n",em[i].info);
        fprintf (fl,"-end\n");
    }
    fclose(fl);
    return 1;
}

int inEvents (event* em) { // загрузить из файла, вернуть количество элементов в массиве
    FILE *fl;
    int n,num; //кол-во прочитанных событий, уникальный номер
    int t1, d1, p1, i1; //признак прочитанных данных
    char sp[50]; //поля события
    char si[100];
    dt dd;
    int t;
    char tmpc;
    char *lbr;  //переменная для сохранения указателя на перенос строки
 
    fl = fopen(EVENTS_FILE, "r");
    if (fl == NULL) {
        printf("Ошибка открытия файла, данные будут сгенерированы\n");
        n=3; //первоначальное заполнение событий вне файла
        for (int i=0;i<n;i++) em[i]=fillEvent(i+1);
        for (int i=n;i<ESIZE;i++) em[i]=emptyEvent();
        return n;
    }
    n=0;//индекс массива событий
    num=1;
    t1=0; d1=0; p1=0; i1=0; //признак успешного считывания ставим 0
    while  (!feof(fl)) {
        tmpc = fgetc(fl);
        if (tmpc=='t') {
            tmpc = fgetc(fl);
            if (tmpc==':') {
                if (fscanf(fl,"%d",&t)==1) if ((t==1)||(t==2)) t1=1;
            }
        }
        
        if (tmpc=='d') {
            tmpc = fgetc(fl);
            if (tmpc==':') 
                if (fscanf(fl,"%d%*c%d%*c%d%*c%d%*c%d",&dd.d,&dd.m,&dd.y,&dd.h,&dd.mn)==5) d1=1;
        }
        if (tmpc=='p') {
            tmpc = fgetc(fl);
            if (tmpc==':')  
                if (fgets(sp,50,fl)!=NULL) {
                    p1=1;
                    lbr = strchr(sp,10); // поиск первого вхождения переноса строки
                    if (lbr!=NULL) { *lbr = 0; } //замена на 0
                }
        }
        if (tmpc=='i') {
            tmpc = fgetc(fl);
            if (tmpc==':')  
                if (fgets(si,100,fl)!=NULL) {
                    i1=1;
                    lbr = strchr(si,10); // поиск первого вхождения переноса строки
                    if (lbr!=NULL) { *lbr = 0; } //замена на 0
                }
        }
        if (tmpc=='-'){
            t1=0; d1=0; p1=0; i1=0;
        }
        if ((t1==1)&&(d1==1)&&(p1==1)&&(i1==1)) {
            em[n++]=setEvent(num++,t,dd,sp,si);
            t1=0; d1=0; p1=0; i1=0; //признак успешного считывания ставим 0
        }
    }
    fclose(fl);
    if(n>0)printf("Успешно загружены события из файла\n");
    if (n==0) { 
        printf("События из файла не загружены, данные будут сгенерированы\n");
        n=3; //если файл пустой
        for (int i=0;i<n;i++) em[i]=fillEvent(i+1);
        for (int i=n;i<ESIZE;i++) em[i]=emptyEvent();
    }
    return n;
}

int main() {
    int cmd=0,num,p=0, n=0; //номер команды, номер события, индекс события кол-во заполненных событий в массиве
    char str[10]; //строка ввода для выхода
    event em [ESIZE]; // массив событий
    n = inEvents(em);
    
    do {
        cmd = choiceMenu(); //вывод меню и получение номера команды
        
        // выбор функции для выполнения команды
        switch (cmd) {
            case 1: //просмотр ближайщих событий
                viewEvents(em,n);
                break;
            case 2:  // период времени с нахождением событий
                periodEvents(em,n);
                break;
            case 3:  // поиск по параметру событие
                searchEvents(em,n);
                break;
            case 4:  // сохранить события в файл
                p=outEvents(em,n);
                if (p==1) printf("Успешно сохранен файл: %s\n", EVENTS_FILE); 
                break;
            case 5:  // новое событие
                if (n<ESIZE) {
                    num=getNum(em,n);
                    em[n]=getEvent(num);
                    printf("Сохранено событие:\n"); 
                    printEvent(em[n++],1);
                } else {printf("Команда не может быть выполнена: достигнуто ограничение по количеству событий\n"); }
                break;
            case 6:  // редактирование события
                p=editEvent(em,n);
                if (p>-1) printEvent(em[p],1);
                break;
            case 7:  // удаление события
                p=delEvent(em,n);
                if (p>-1) {
                    n--;
                    printf("Событие успешно удалено\n"); 
                }
                break;
            case 8:  // получение событий из файла
                n = inEvents(em);
                
                break;
            default:
                printf ("Ошибка. Для выхода нажмите \"y\": ");
                scanf("%10s",str);
                while ((getchar()) != '\n');//очищение потока ввода
                if (strcmp(str,"y")==0) cmd=0;
                else cmd=-1;
        }
    } while (cmd !=0);
    outEvents(em,n);
    return 0;
}
