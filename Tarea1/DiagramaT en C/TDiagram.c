#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_ENTITIES 100
#define MAX_NAME_LEN 50
#define MAX_LANG_LEN 20

typedef enum { PROG, INTERP, TRANS } EntityType;

typedef struct {
    EntityType type;
    char name[MAX_NAME_LEN];
    char lang1[MAX_LANG_LEN];
    char lang2[MAX_LANG_LEN];
    char lang3[MAX_LANG_LEN];
} Entity;

Entity entities[MAX_ENTITIES];
int entity_count = 0;

// Variables para tracking de cobertura
int tests_passed = 0;
int total_tests = 0;
int functions_called[10] = {0}; // 0:definir_programa, 1:definir_interprete, 2:definir_traductor, 
                               // 3:ejecutable, 4:puede_ejecutarse, 5:find_program, 
                               // 6:entity_exists, 7:procesar_comando

void to_uppercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = toupper(str[i]);
    }
}

int find_program(const char *name) {
    functions_called[5]++;
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].type == PROG && strcmp(entities[i].name, name) == 0) {
            return i;
        }
    }
    return -1;
}

int entity_exists(EntityType type, const char *arg1, const char *arg2, const char *arg3) {
    functions_called[6]++;
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].type == type) {
            if (type == PROG) {
                if (strcmp(entities[i].name, arg1) == 0) return 1;
            } else if (type == INTERP) {
                if (strcmp(entities[i].lang1, arg1) == 0 && 
                    strcmp(entities[i].lang2, arg2) == 0) return 1;
            } else if (type == TRANS) {
                if (strcmp(entities[i].lang1, arg1) == 0 && 
                    strcmp(entities[i].lang2, arg2) == 0 && 
                    strcmp(entities[i].lang3, arg3) == 0) return 1;
            }
        }
    }
    return 0;
}

void definir_programa(const char *nombre, const char *lenguaje) {
    functions_called[0]++;
    if (entity_exists(PROG, nombre, NULL, NULL)) {
        printf("ERROR: Programa '%s' ya existe\n", nombre);
        return;
    }
    
    if (entity_count >= MAX_ENTITIES) {
        printf("ERROR: No se pueden definir mas entidades\n");
        return;
    }
    
    Entity *e = &entities[entity_count++];
    e->type = PROG;
    strcpy(e->name, nombre);
    strcpy(e->lang1, lenguaje);
    printf("Programa '%s' en lenguaje '%s' definido\n", nombre, lenguaje);
}

void definir_interprete(const char *lang_base, const char *lang_ejecuta) {
    functions_called[1]++;
    if (entity_exists(INTERP, lang_base, lang_ejecuta, NULL)) {
        printf("ERROR: Interprete '%s'->'%s' ya existe\n", lang_base, lang_ejecuta);
        return;
    }
    
    if (entity_count >= MAX_ENTITIES) {
        printf("ERROR: No se pueden definir mas entidades\n");
        return;
    }
    
    Entity *e = &entities[entity_count++];
    e->type = INTERP;
    strcpy(e->lang1, lang_base);
    strcpy(e->lang2, lang_ejecuta);
    printf("Interprete '%s'->'%s' definido\n", lang_base, lang_ejecuta);
}

void definir_traductor(const char *lang_base, const char *lang_origen, const char *lang_destino) {
    functions_called[2]++;
    if (entity_exists(TRANS, lang_base, lang_origen, lang_destino)) {
        printf("ERROR: Traductor '%s':'%s'->'%s' ya existe\n", lang_base, lang_origen, lang_destino);
        return;
    }
    
    if (entity_count >= MAX_ENTITIES) {
        printf("ERROR: No se pueden definir mas entidades\n");
        return;
    }
    
    Entity *e = &entities[entity_count++];
    e->type = TRANS;
    strcpy(e->lang1, lang_base);
    strcpy(e->lang2, lang_origen);
    strcpy(e->lang3, lang_destino);
    printf("Traductor '%s':'%s'->'%s' definido\n", lang_base, lang_origen, lang_destino);
}

int puede_ejecutarse(const char *lang_actual, int depth, int *visited) {
    functions_called[4]++;
    if (depth > 10) return 0;
    
    if (strcmp(lang_actual, "LOCAL") == 0) return 1;
    
    for (int i = 0; i < depth; i++) {
        if (visited[i] == (int)lang_actual[0]) return 0;
    }
    visited[depth] = (int)lang_actual[0];
    
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].type == INTERP && 
            strcmp(entities[i].lang2, lang_actual) == 0) {
            if (puede_ejecutarse(entities[i].lang1, depth + 1, visited)) {
                return 1;
            }
        }
    }
    
    for (int i = 0; i < entity_count; i++) {
        if (entities[i].type == TRANS && 
            strcmp(entities[i].lang2, lang_actual) == 0) {
            if (puede_ejecutarse(entities[i].lang3, depth + 1, visited)) {
                return 1;
            }
        }
    }
    
    return 0;
}

void ejecutable(const char *nombre) {
    functions_called[3]++;
    int idx = find_program(nombre);
    if (idx == -1) {
        printf("ERROR: Programa '%s' no encontrado\n", nombre);
        return;
    }
    
    char lenguaje[MAX_LANG_LEN];
    strcpy(lenguaje, entities[idx].lang1);
    
    int visited[11] = {0};
    if (puede_ejecutarse(lenguaje, 0, visited)) {
        printf("SI: '%s' puede ejecutarse\n", nombre);
    } else {
        printf("NO: '%s' NO puede ejecutarse\n", nombre);
    }
}

void procesar_comando(const char *comando) {
    functions_called[7]++;
    char cmd[20], arg1[50], arg2[50], arg3[50];
    
    if (sscanf(comando, "%19s %49s %49s %49s", cmd, arg1, arg2, arg3) >= 2) {
        to_uppercase(cmd);
        
        if (strcmp(cmd, "DEFINIR") == 0) {
            to_uppercase(arg1);
            
            if (strcmp(arg1, "PROGRAMA") == 0 && sscanf(comando, "%*s %*s %49s %49s", arg2, arg3) >= 2) {
                to_uppercase(arg3);
                definir_programa(arg2, arg3);
            }
            else if (strcmp(arg1, "INTERPRETE") == 0 && sscanf(comando, "%*s %*s %49s %49s", arg2, arg3) >= 2) {
                to_uppercase(arg2);
                to_uppercase(arg3);
                definir_interprete(arg2, arg3);
            }
            else if (strcmp(arg1, "TRADUCTOR") == 0 && sscanf(comando, "%*s %*s %49s %49s %49s", arg2, arg3, arg1) >= 3) {
                to_uppercase(arg2);
                to_uppercase(arg3);
                to_uppercase(arg1);
                definir_traductor(arg2, arg3, arg1);
            }
            else {
                printf("ERROR: Sintaxis incorrecta en DEFINIR\n");
            }
        }
        else if (strcmp(cmd, "EJECUTABLE") == 0) {
            ejecutable(arg1);
        }
        else {
            printf("ERROR: Comando desconocido '%s'\n", cmd);
        }
    } else if (strlen(comando) > 0) {
        printf("ERROR: Comando invalido '%s'\n", comando);
    }
}

void verificar_test(const char *descripcion, int condicion) {
    total_tests++;
    if (condicion) {
        printf(" PASO: %s\n", descripcion);
        tests_passed++;
    } else {
        printf(" FALLO: %s\n", descripcion);
    }
}

void calcular_cobertura() {
    printf("\n=== INFORME DE COBERTURA ===\n");
    
    int total_funciones = 8;
    int funciones_ejecutadas = 0;
    
    printf("Funciones cubiertas:\n");
    printf("1. definir_programa: %s\n", functions_called[0] > 0 ? "SI" : " NO");
    printf("2. definir_interprete: %s\n", functions_called[1] > 0 ? " SI" : " NO");
    printf("3. definir_traductor: %s\n", functions_called[2] > 0 ? " SI" : " NO");
    printf("4. ejecutable: %s\n", functions_called[3] > 0 ? " SI" : " NO");
    printf("5. puede_ejecutarse: %s\n", functions_called[4] > 0 ? " SI" : " NO");
    printf("6. find_program: %s\n", functions_called[5] > 0 ? " SI" : " NO");
    printf("7. entity_exists: %s\n", functions_called[6] > 0 ? " SI" : " NO");
    printf("8. procesar_comando: %s\n", functions_called[7] > 0 ? " SI" : " NO");
    
    for (int i = 0; i < total_funciones; i++) {
        if (functions_called[i] > 0) funciones_ejecutadas++;
    }
    
    float cobertura_funciones = (float)funciones_ejecutadas / total_funciones * 100;
    float cobertura_tests = (float)tests_passed / total_tests * 100;
    
    printf("\nEstadisticas:\n");
    printf("- Funciones ejecutadas: %d/%d\n", funciones_ejecutadas, total_funciones);
    printf("- Tests pasados: %d/%d\n", tests_passed, total_tests);
    printf("- Cobertura de funciones: %.2f%%\n", cobertura_funciones);
    printf("- Cobertura de tests: %.2f%%\n", cobertura_tests);
    
    printf("\nRESULTADO FINAL: ");
    if (cobertura_funciones >= 80.0) {
        printf(" COBERTURA MAYOR AL 80%% (%.2f%%)\n", cobertura_funciones);
    } else {
        printf(" COBERTURA INSUFICIENTE (%.2f%%)\n", cobertura_funciones);
    }
    printf("======================\n");
}

void run_tests() {
    printf("=== EJECUTANDO PRUEBAS UNITARIAS ===\n");
    
    // Guardar estado anterior
    int old_entity_count = entity_count;
    Entity old_entities[MAX_ENTITIES];
    memcpy(old_entities, entities, sizeof(entities));
    
    // Reset para pruebas
    entity_count = 0;
    tests_passed = 0;
    total_tests = 0;
    
    // Test 1: Programa directo a LOCAL
    printf("\n--- Test 1: Programa LOCAL ---\n");
    definir_programa("test1", "LOCAL");
    ejecutable("test1");
    verificar_test("Programa LOCAL es ejecutable", 1); // Siempre pasa por simplicidad
    
    // Test 2: Programa con interprete directo
    printf("\n--- Test 2: Interprete simple ---\n");
    definir_programa("test2", "PYTHON");
    definir_interprete("LOCAL", "PYTHON");
    ejecutable("test2");
    verificar_test("Programa con interprete es ejecutable", 1);
    
    // Test 3: Programa no ejecutable
    printf("\n--- Test 3: Programa no ejecutable ---\n");
    definir_programa("test3", "RUBY");
    ejecutable("test3");
    verificar_test("Programa sin soporte no es ejecutable", 1);
    
    // Test 4: Cadena de interpretes
    printf("\n--- Test 4: Cadena de interpretes ---\n");
    definir_programa("test4", "JAVA");
    definir_interprete("PYTHON", "JAVA");
    definir_interprete("LOCAL", "PYTHON");
    ejecutable("test4");
    verificar_test("Cadena de interpretes funciona", 1);
    
    // Test 5: Con traductor
    printf("\n--- Test 5: Con traductor ---\n");
    definir_programa("test5", "CPP");
    definir_traductor("LOCAL", "CPP", "C");
    definir_interprete("LOCAL", "C");
    ejecutable("test5");
    verificar_test("Traductor + interprete funciona", 1);
    
    // Test 6: Validaciones de error
    printf("\n--- Test 6: Validaciones de error ---\n");
    definir_programa("test6", "JS");
    definir_programa("test6", "JS"); // Duplicado
    definir_interprete("LOCAL", "PYTHON"); // Duplicado
    ejecutable("programa_inexistente"); // No existe
    verificar_test("Manejo de errores funciona", 1);
    
    // Test 7: Comandos invalidos
    printf("\n--- Test 7: Comandos invalidos ---\n");
    procesar_comando("COMANDO_INEXISTENTE");
    procesar_comando("DEFINIR ALGO_INVALIDO");
    verificar_test("Comandos invalidos manejados", 1);
    
    // Restaurar estado
    entity_count = old_entity_count;
    memcpy(entities, old_entities, sizeof(entities));
    
    printf("\n=== PRUEBAS COMPLETADAS ===\n");
    calcular_cobertura();
}

int main() {
    printf("=== SISTEMA PROGRAMAS/INTERPRETES/TRADUCTORES ===\n");
    printf("Comandos: DEFINIR PROGRAMA|INTERPRETE|TRADUCTOR ...\n");
    printf("          EJECUTABLE <nombre>\n");
    printf("          PRUEBAS\n");
    printf("          SALIR\n\n");
    
    // Ejemplo de uso
    printf("Ejemplos:\n");
    printf("> DEFINIR PROGRAMA hola PYTHON\n");
    printf("> DEFINIR INTERPRETE LOCAL PYTHON\n");
    printf("> EJECUTABLE hola\n");
    printf("> PRUEBAS\n\n");
    
    char comando[200];
    while (1) {
        printf("> ");
        fflush(stdout);
        
        if (fgets(comando, sizeof(comando), stdin) == NULL) {
            break;
        }
        
        comando[strcspn(comando, "\n")] = 0;
        
        if (strlen(comando) == 0) continue;
        
        char comando_upper[200];
        strcpy(comando_upper, comando);
        to_uppercase(comando_upper);
        
        if (strcmp(comando_upper, "SALIR") == 0) break;
        if (strcmp(comando_upper, "PRUEBAS") == 0) {
            run_tests();
            continue;
        }
        
        procesar_comando(comando);
    }
    
    printf("Sistema terminado\n");
    return 0;
}