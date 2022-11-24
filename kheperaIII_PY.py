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


class Strategies():

    def __init__(self, robot):
        self.robot = robot
        self.task_time = 0

        
    def devices_value(self, device):
        """ Método de classe que irá pegar o valor lido pelo sensor"""
        
        return self.robot.devices[device].getValue()
    
    
    def update_sensor(self):
        
        """ Método de classe que irá definir os sensores e atualiza-los
        
        *É necessário ser utilizado no inicio de cada estratégia, para os valores
        dos sensores serem atualizados        
        
        iflf = sensor infravermelho esquerdo
        ifrg = sensor infravermelho direito
        ultrg = sensor ultrassonico direito
        ultlf = sensor ultrassonico esquerdo
        ultfr = sensor ultrassonico frontal
        time = tempo decorrido
        
        """
        
        self.iflf = self.devices_value('left_infra_red')
        self.ifrg = self.devices_value('right_infra_red')
        self.ultrg = self.devices_value('ultrassound_right')
        self.ultlf = self.devices_value('ultrassound_left')
        self.ultfr = self.devices_value('ultrassound_front')
        self.time = self.robot.robot.getTime()
    
            
    def strategy_1(self):
    
        """ Seguir em frente até achar o inimigo
        
        Estratégia padrão do mini-sumo, ele irá seguir em linha reta até encontrar
        o robo adversário ou encontrar as bordas da arena
        """

        self.update_sensor()
  
        if self.iflf > 2000 and self.time - self.task_time > 0.5:
            self.task_time = self.time           
            self.robot.state = 'RIGHT'
            
        elif self.ifrg > 2000 and self.time - self.task_time > 0.5:
            self.task_time = self.time
            self.robot.state = 'LEFT'
            
        elif self.ultfr > 500:
            self.robot.state = 'FORWARD'
        
        elif self.ultlf > 500:
            self.robot.state = 'FORWARD_LEFT'
        
        elif self.ultrg > 500:
            self.robot.state = 'FORWARD_RIGHT'
     
        elif self.time - self.task_time > 0.5:
            self.robot.state = 'FORWARD'
            
    def strategy_2(self):
        """ Tenta dar a volta no inimigo e empurra-lo pelo lado/por tras
        
        O mini-sumo deve começar virado para uma borda da arena, para então ele fazer uma 
        curvatura até encontrar o adversário. A quantidade de vezes que esse comportamento 
        é adotado é controlado pela variável "c", caso o limite seja atingido ele seguirá o 
        comportamento padrão
        
        """
        self.update_sensor()
        c = 0
        if c == 0:
            if self.ultlf > 500:
                self.robot.state = 'FORWARD_LEFT'
                c += 1
                
                
            elif self.ultrg > 500:
                self.robot.state = 'FORWARD_RIGHT'
                c += 1
    
            elif self.ifrg > 2000: 
                self.robot.state = 'LEFT'
    
                 
            elif self.iflf > 2000:
                self.robot.state = 'RIGHT'
    
                
            else: 
                robot.state = 'FORWARD'
                
        else:
           self.strategy_1()
    
    def strategy_3(self):
        """ Em andamento
        
        Consiste em fazer o robo ir dando uns "pulinhos" até o sensor detectar o adversário,
        então fazer o robo ir com velocidade máxima para cima do inimigo
        
        
        """
    
        self.update_sensor()
        
        if self.ultf == 0:
            self.task_time = self.time
        
        
        if self.iflf > 2000 and self.time - self.task_time > 0.5:
            self.task_time = self.time           
            self.robot.state = 'RIGHT'
            
        elif self.ifrg > 2000 and self.time - self.task_time > 0.5:
            self.task_time = self.time
            self.robot.state = 'LEFT'
            
            
            
        

if __name__ == '__main__':
 
    robot = stateMachine(Robot())
    s = Strategies(robot)
    while robot.robot.step(TIME_STEP) != -1: #Insira dentro desse laço while o código que rodará continuamente (estilo loop do arduino)
        
  
        s.strategy_1()
        pass
        
