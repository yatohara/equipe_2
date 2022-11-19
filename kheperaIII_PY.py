from controller import Robot, Motor, DistanceSensor
TIME_STEP = 32
MAX_SPEED = 12


#Listas de equipamentos do robo - CADA DEVICE DEVE TER UMA INSTANCE VINCULADA
#Devices sao os equipamentos dentro do robo
DEVICES = ['left wheel motor', 'right wheel motor', 'ds10', 'ds9', 'us1', 'us2', 'us3']
#Instances são os nomes das instancias de cada device EM ORDEM
INSTANCES = ['left_wheel', 'right_wheel', 'left_infra_red', 'right_infra_red', 'ultrassound_right', 'ultrassound_front', 'ultrassound_left']


#abordagem por maquina de estados
class stateMachine:
    def __init__(self, robot):
        self.robot = robot
        self.state = 'DEFAULT'
        
        #faz um dicionario com as instancias e devices
        self.devices = dict(zip(INSTANCES, DEVICES))
        for x in self.devices.keys():
            if 'wheel' in x: #encontrando uma variavel de motor
                vars()[x] = self.robot.getDevice(self.devices[x]) #cria a variavel com o nome colocado na lista INSTANCES
                self.devices[x] = vars()[x]
                
                self.devices[x].setPosition(float('inf')) #inicializa o motor
                self.devices[x].setVelocity(0.0)
                
            elif 'infra_red' in x or 'ultrassound' in x: #faz o mesmo com sensores
                vars()[x] = self.robot.getDevice(self.devices[x])
                self.devices[x] = vars()[x]
                
                self.devices[x].enable(TIME_STEP)
    
    
    # Para facilitar os possíveis casos de movimento
    def wheels_velocity(self, right_speed, left_speed):
        self.devices['right_wheel'].setVelocity(right_speed)
        self.devices['left_wheel'].setVelocity(left_speed)
    
    
                
    def process(self): #processamento dos estados
        default = 'Error in Machine State' #mensagem de erro
       
        #"switch case" do python                    
        return getattr(self, 'case_' + str(self.state), lambda: default)()
        
    def case_FORWARD(self): #andar para frente
        self.wheels_velocity(MAX_SPEED, MAX_SPEED)

    def case_BACK(self): #andar para tras
        self.wheels_velocity(-MAX_SPEED, -MAX_SPEED)

    def case_LEFT(self): #virar para a direita
        self.wheels_velocity(MAX_SPEED, -MAX_SPEED)

        
    def case_RIGHT(self): #virar para a esquerda
        self.wheels_velocity(-MAX_SPEED, MAX_SPEED)
        
    def case_FORWARD_RIGHT(self):
        self.wheels_velocity(MAX_SPEED, 0.25 * MAX_SPEED)

    def case_FORWARD_LEFT(self):
        self.wheels_velocity(0.25 * MAX_SPEED, MAX_SPEED)        
    
c = 0
last_instruction = 0
if __name__ == '__main__':
 
    robot = stateMachine(Robot())
         
    while robot.robot.step(TIME_STEP) != -1: #Insira dentro desse laço while o código que rodará continuamente (estilo loop do arduino)
        
        current_time = robot.robot.getTime()
        infraL_value = robot.devices['left_infra_red'].getValue()
        infraR_value = robot.devices['right_infra_red'].getValue()
        ultra_direita = robot.devices['ultrassound_right'].getValue()
        ultra_frente = robot.devices['ultrassound_front'].getValue()
        ultra_esquerda = robot.devices['ultrassound_left'].getValue()
        
        # Movimentação padrão
        
        # if ultra_esquerda > 500:
            # robot.state = 'FORWARD_LEFT'
            # print('Ultra esquerda')
        # elif ultra_direita > 500:
            # robot.state = 'FORWARD_RIGHT'
            # print('Ultra direita')
        # elif ultra_frente > 500:
            # robot.state = 'FORWARD'
            # print('Ultra frente')
        # elif infraL_value > 2000 and current_time - last_instruction > 0.5:
            # last_instruction = current_time
            # robot.state = 'RIGHT'
        # elif infraR_value > 2000 and current_time - last_instruction > 0.5:
            # last_instruction = current_time
            # robot.state = 'LEFT'
        # elif current_time - last_instruction > 0.5:
            # robot.state = 'FORWARD'
            
            
        # Tentar dar a volta e empurrar
        
        
        """
        O robo está contornando a borda da arena e buscando o seu oponente. Falhas encontradas:
            - Alcance dos sensores, o adversário tem que estar extramemente próximo das bordas
            - O robo fica mais vulnerável
        
        Talvez se fosse possível detectar a localização exata do outro robo no inicio da partida
        seria possível calcular uma trajetória em forma de arco, em vez de contornar as bordas.
        
        Da forma que está é possível o robo começar apontado para a linha branca, ou voltado para
        os lados, já que no momento que ele encontrar a linha ele vai contorna-la.
             
        """
        if c == 0:  # Essa flag seria para esse movimento só se repetir uma vez e após isso o robo voltar a ter a sua movimentação padrão
            if ultra_esquerda > 500:
                robot.state = 'FORWARD_LEFT'
                c += 1
                
            elif ultra_direita > 500:
                robot.state = 'FORWARD_RIGHT'
                c += 1
                
            elif infraR_value > 2000: 
                robot.state = 'LEFT'

                 
            elif infraL_value > 2000:
                robot.state = 'RIGHT'

                
            else: 
                robot.state = 'FORWARD'
                
        robot.process() #processa o estado
