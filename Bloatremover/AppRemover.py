import subprocess
import time
import datetime

class Device:
    def __init__(self):
        self.connected = False

    # Verifica se o dispositivo Android está conectado
    def check_connected(self):
        devices_cmd = ['adb', 'devices']
        output = subprocess.check_output(devices_cmd).decode()
        if 'device' in output:
            print('Dispositivo Android conectado.')
            self.connected = True
        else:
            print('Erro: Dispositivo desconectado.')
            self.connected = False

    def is_connected(self):
        return self.connected

class BloatHandler:
    def __init__(self):
        self.action = None
        self.device = Device()
        self.log_filename = f'bloat_handler_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    # Lê a lista de pacotes do arquivo bloat.txt
    def read_bloat_list(self):
        bloat_list = []
        with open('bloat.txt', 'r') as f:
            for line in f:
                package = line.strip()
                if package:
                    bloat_list.append(package)
        return bloat_list

    # Remove ou instala um pacote no dispositivo
    def process_package(self, package, action):
        if action == 'remove':
            cmd = ['adb', 'shell', 'pm', 'uninstall', '--user', '0', package]
            success_msg = f'Pacote {package} removido com sucesso.'
            error_msg = f'Erro ao remover pacote {package}.'
        elif action == 'install':
            cmd = ['adb', 'shell', 'cmd', 'package', 'install-existing', package]
            success_msg = f'Pacote {package} instalado com sucesso.'
            error_msg = f'Erro ao instalar pacote {package}.'

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0:
            time.sleep(0.4)
            message = success_msg
            print(success_msg)
        else:
            time.sleep(0.4)
            message = error_msg
            print(error_msg)
            message += '\n' + result.stderr.decode()
        self.log(message)

    # Processa a lista de pacotes para remoção ou instalação
    def process_bloat(self, action):
        if not self.device.is_connected():
            return
        bloat_list = self.read_bloat_list()
        for package in bloat_list:
            self.process_package(package, action)

    # Escreve uma mensagem no arquivo de log
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_filename, 'a') as f:
            f.write(f'[{timestamp}] {message}\n')

    # Chamada principal do programa
    def run(self, action):
        self.device.check_connected()
        self.action = action
        self.process_bloat(action)
