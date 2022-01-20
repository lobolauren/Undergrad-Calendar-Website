commands = []
correct_input = 0
incorrect_coursesearch = False
while correct_input <= 0:
    # Reset flags
    correct_input = 0
    incorrect_coursesearch = False

    # User input
    commands = input("Course search: ").split()

    # Quit CLI program
    if commands[0] == "quit" or commands[0] == "exit":
        break

    # "coursesearch" (must be first argument if included)
    if commands[0] == "coursesearch":
        correct_input += 1
    else:
        for i in range(len(commands)):
            if commands[i] == "coursesearch":
                correct_input = 0
                incorrect_coursesearch = True

    # Course name (keyword such as: programming, algebra, chemistry)

    # Course code (acceptable input examples: CIS*1300, CIS, 1300)
    for command in commands:
        if command >= 1000: # course code number will always be >= 1000
            correct_input += 1

    # Weight (must be a decimal value)
    for command in commands:
        try:
            float(command)
            correct_input += 1
        except ValueError:
            continue

    # Season (either S, F, or W)
    for command in commands:
        if command == 'S' or command == 's' or command == 'F' or command == 'f' or command == 'W' or command == 'w':
            correct_input += 1

    # Minimum command-line arguments required: 2 (coursesearch + argument). Maximum: 5
    if incorrect_coursesearch == True:
        print("'coursesearch' must be the first argument")
        correct_input = 0
    if correct_input < 2:
        print("Too few arguments.")
        correct_input = 0
    elif correct_input > 5:
        print("Too many arguments.")
        correct_input = 0
print(commands)
