# --- CONFIGURACIÓN GENERAL ---
CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -g -fprofile-instr-generate -fcoverage-mapping
SRC = src/vector3.cpp
TEST = tests/test_vector3.cpp
OUT = vector3_test
PROFRAW = $(OUT).profraw
PROFDATA = $(OUT).profdata

# --- REGLAS PRINCIPALES ---
all: run coverage

$(OUT): $(SRC) $(TEST)
	@echo "🔧 Compilando con cobertura..."
	$(CXX) $(CXXFLAGS) $(SRC) $(TEST) -I./src -o $(OUT)
	@echo "Compilación completa."

run: $(OUT)
	@echo "Ejecutando pruebas..."
	LLVM_PROFILE_FILE=$(PROFRAW) ./$(OUT)

coverage: $(OUT)
	@echo "Ejecutando pruebas para cobertura..."
	LLVM_PROFILE_FILE=$(PROFRAW) ./$(OUT)
	@echo "Generando datos de cobertura..."
	llvm-profdata merge -sparse $(PROFRAW) -o $(PROFDATA)
	@echo "Reporte de cobertura:"
	llvm-cov report ./$(OUT) -instr-profile=$(PROFDATA) src/

# --- LIMPIEZA ---
clean:
	@echo "Limpiando archivos generados..."
	rm -f $(OUT) $(PROFRAW) $(PROFDATA)
