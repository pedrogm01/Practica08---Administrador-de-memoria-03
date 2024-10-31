import os

def leer_archivos_desde_txt(filename):
    file_sizes = []
    with open(filename, 'r') as f:
        for line in f:
            nombre, size = line.split(',')
            size = int(size.strip().replace('kb', ''))  # Convertir el tamaño a entero
            file_sizes.append((nombre.strip(), size))  # Guardar como una tupla (nombre, tamaño)
    return file_sizes

def agregar_bloque(memory_blocks):
    size = int(input("Ingrese el tamaño del bloque de memoria (en KB): "))
    status = input("Ingrese el estado del bloque (Disponible/Ocupado): ").lower()
    position = input("Ingrese la posición (Inicio/Final): ").lower()

    if position == "inicio":
        memory_blocks.insert(0, size if status == "disponible" else 0)
    else:
        memory_blocks.append(size if status == "disponible" else 0)

def agregar_archivo_virtual(file_sizes):
    name = input("Ingrese el nombre del archivo: ")
    size = int(input("Ingrese el tamaño del archivo (en KB): "))
    position = input("Ingrese la posición (Inicio/Final): ").lower()

    if position == "inicio":
        file_sizes.insert(0, (name, size))
    else:
        file_sizes.append((name, size))

def seleccionar_archivos(file_sizes):
    while True:
        print("\n1. Leer archivos desde archivos.txt")
        print("2. Agregar archivo virtual")
        print("3. Agregar archivo físico")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            file_sizes.extend(leer_archivos_desde_txt('archivos.txt'))
        elif choice == '2':
            agregar_archivo_virtual(file_sizes)
        elif choice == '3':
            filename = input("Ingrese el nombre del archivo físico (con extensión): ")
            if os.path.exists(filename):
                size = os.path.getsize(filename) // 1024  # Convertir bytes a KB
                file_sizes.append((filename, size))
            else:
                print("Archivo no encontrado.")
        else:
            print("Opción no válida.")
            continue

        if input("¿Desea agregar más archivos? (s/n): ").lower() != 's':
            break

def first_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        assigned = False
        for i, block in enumerate(memory_blocks):
            if block >= file_size:
                assignments.append((file_name, file_size, block))
                memory_blocks[i] -= file_size  # Actualizamos el bloque de memoria disponible
                assigned = True
                break
        if not assigned:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def best_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        best_index = None
        best_fit_size = float('inf')
        for i, block in enumerate(memory_blocks):
            if block >= file_size and block < best_fit_size:
                best_fit_size = block
                best_index = i
        if best_index is not None:
            assignments.append((file_name, file_size, memory_blocks[best_index]))
            memory_blocks[best_index] -= file_size  # Actualizamos el bloque de memoria disponible
        else:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def worst_fit(memory_blocks, file_sizes):
    assignments = []
    for file_name, file_size in file_sizes:
        worst_index = None
        worst_fit_size = -1
        for i, block in enumerate(memory_blocks):
            if block >= file_size and block > worst_fit_size:
                worst_fit_size = block
                worst_index = i
        if worst_index is not None:
            assignments.append((file_name, file_size, memory_blocks[worst_index]))
            memory_blocks[worst_index] -= file_size  # Actualizamos el bloque de memoria disponible
        else:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def next_fit(memory_blocks, file_sizes):
    assignments = []
    start_index = 0  # Recordar el último bloque donde se realizó una asignación
    for file_name, file_size in file_sizes:
        assigned = False
        for i in range(start_index, len(memory_blocks)):
            if memory_blocks[i] >= file_size:
                assignments.append((file_name, file_size, memory_blocks[i]))
                memory_blocks[i] -= file_size
                start_index = i  # Actualizamos el índice de inicio para la próxima asignación
                assigned = True
                break
        if not assigned:
            assignments.append((file_name, file_size, None))  # No se encontró un bloque adecuado
    return assignments

def show_results(assignments):
    print("\n")
    for file_name, file_size, block in assignments:
        if block is not None:
            print(f"El archivo '{file_name}' de {file_size} Kb fue asignado al bloque de {block} Kb.")
        else:
            print(f"El archivo '{file_name}' de {file_size} Kb no pudo ser asignado a ningún bloque.")

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    memory_blocks = [1000, 400, 1800, 700, 900, 1200, 1500]
    file_sizes = []

    while True:
        print("\n1. Ver bloques de memoria")
        print("2. Agregar bloque de memoria")
        print("3. Seleccionar archivos a asignar")
        print("4. Seleccionar algoritmo de asignación")
        print("5. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            print("\nBloques de memoria disponibles:", memory_blocks)
        elif choice == '2':
            agregar_bloque(memory_blocks)
        elif choice == '3':
            seleccionar_archivos(file_sizes)
        elif choice == '4':
            if not file_sizes:
                print("No hay archivos seleccionados.")
                continue

            print("\nSeleccione el algoritmo de asignación de memoria:")
            print("1. Primer ajuste")
            print("2. Mejor ajuste")
            print("3. Peor ajuste")
            print("4. Siguiente ajuste")
            alg_choice = int(input("Opción: "))

            if alg_choice == 1:
                assignments = first_fit(memory_blocks[:], file_sizes)
            elif alg_choice == 2:
                assignments = best_fit(memory_blocks[:], file_sizes)
            elif alg_choice == 3:
                assignments = worst_fit(memory_blocks[:], file_sizes)
            elif alg_choice == 4:
                assignments = next_fit(memory_blocks[:], file_sizes)
            else:
                print("Opción no válida.")
                continue

            show_results(assignments)
        elif choice == '5':
            break
        else:
            print("Opción no válida.")

        if input("\n¿Desea continuar? (s/n): ").lower() != 's':
            break

if __name__ == "__main__":
    main()
