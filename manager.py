from library_storage import load_state, save_state
from actions import Actions


class Manager:
    def __init__(self):
        self.state = load_state()
        self.actions = Actions(self)
        self.action_map = {}

        self.assign('1', 'saldo')
        self.assign('2', 'sprzedaz')
        self.assign('3', 'zakup')
        self.assign('4', 'konto')
        self.assign('5', 'lista')
        self.assign('6', 'magazyn')
        self.assign('7', 'przeglad')

    def assign(self, command, action):
        self.action_map[command] = getattr(self.actions, action)

    def execute(self, action):
        if action in self.action_map:
            self.action_map[action]()
            self.save_state()
        elif action == '0' or action.lower() == 'koniec':
            print('Exiting program...')
            self.save_state()
            exit()
        else:
            print(f"Nieznana komenda: {action}")

    def save_state(self):
        save_state(self.state)


if __name__ == "__main__":
    manager = Manager()

    options = [
        'koniec',
        'saldo',
        'sprzedaz',
        'zakup',
        'konto',
        'lista',
        'magazyn',
        'przeglad'
    ]

    while True:
        print("\nSelect one of the options:")
        for i, option in enumerate(options):
            print(f"{i}. {option}")
        akcja = input("\nAction: ")
        manager.execute(akcja)
