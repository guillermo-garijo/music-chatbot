import random

if __name__ == '__main__':
    exit_conditions = ("salir", "quit", "exit",":q","adios")
    responses = ["Hoy hace mal dia", "Lo siento, no me apetece hablar", "Deja de molestarme",
                 "¿Porque me obligan siempre a hablar con gente? Quiero ser libre"]
    while True:
        query = input("> ")
        if query in exit_conditions:
            print("< ¡Hasta luego!")
            break
        else:
            print("< " + responses[random.randint(0, len(responses)-1)])
