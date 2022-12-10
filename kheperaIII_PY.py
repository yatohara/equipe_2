from controller import Robot, Motor, DistanceSensor
from math import pi

TIME_STEP = 16
MAX_SPEED = 14

# Listas de equipamentos do robo - CADA DEVICE DEVE TER UMA INSTANCE VINCULADA
# Devices sao os equipamentos dentro do robo
DEVICES = ['left motor', 'right motor', 'left sensor', 'right sensor', 'forward left sensor', 'forward right sensor',
           'front sensor', 'left line sensor', 'right line sensor']
# Instances são os nomes das instancias de cada device EM ORDEM
INSTANCES = ['left_wheel', 'right_wheel', 'left_sensor', 'right_sensor', 'forward_left_sensor', 'forward_right_sensor',
             'front_sensor', 'left_line_sensor', 'right_line_sensor']


# abordagem por maquina de estados
class stateMachine:
    def __init__(self, robot):
        self.robot = robot
        self.state = 'DEFAULT'

        self.devices = dict()
        for dev, inst in zip(DEVICES, INSTANCES):
            if 'wheel' in inst:
                self.devices[inst] = self.robot.getDevice(dev)

                self.devices[inst].setPosition(float('inf'))
                self.devices[inst].setVelocity(0.0)
                print(dev + ' set up')

            elif 'sensor' in inst:
                self.devices[inst] = self.robot.getDevice(dev)

                self.devices[inst].enable(TIME_STEP)
                print(dev + ' set up')

    # Para facilitar os possíveis casos de movimento
    def wheels_velocity(self, right_speed, left_speed):
        self.devices['right_wheel'].setVelocity(right_speed)
        self.devices['left_wheel'].setVelocity(left_speed)

    def process(self):  # processamento dos estados
        default = 'Error in Machine State'  # mensagem de erro

        # "switch case" do python
        return getattr(self, 'case_' + str(self.state), lambda: default)()

    def case_FORWARD(self):  # andar para frente
        self.wheels_velocity(MAX_SPEED, MAX_SPEED)

    def case_BACK(self):  # andar para tras
        self.wheels_velocity(-MAX_SPEED, -MAX_SPEED)

    def case_LEFT(self):  # virar para a esquerda
        self.wheels_velocity(-MAX_SPEED, MAX_SPEED)

    def case_RIGHT(self):  # virar para a direita
        self.wheels_velocity(MAX_SPEED, -MAX_SPEED)

    def case_FORWARD_RIGHT(self):
        self.wheels_velocity(14, 0.1 * 12)

    def case_FORWARD_LEFT(self):
        self.wheels_velocity(0.1 * 12, 14)

    def case_STOP(self):
        self.wheels_velocity(0, 0)

    def case_ARC_RIGHT(self):
        self.wheels_velocity(20, 0.8 * 20)

    def case_ARC_LEFT(self):
        self.wheels_velocity(0.8 * 20, 20)

    def case_VRUM(self):
        """Situação exagerada de overvolted"""
        self.wheels_velocity(40, 40)


class Strategies:
    def __init__(self, robot):
        self.robot = robot
        self.task_time = 0
        self.T = 0.5
        self.c = 0

    def devices_value(self, device):
        return self.robot.devices[device].getValue()

    def update_sensor(self):

        self.time = self.robot.robot.getTime()
        self.left_line_value = self.devices_value('left_line_sensor')
        self.right_line_value = self.devices_value('right_line_sensor')
        self.right_presence_value = self.devices_value('right_sensor')
        self.front_presence_value = self.devices_value('front_sensor')
        self.left_presence_value = self.devices_value('left_sensor')
        self.forward_left_presence_value = self.devices_value('forward_left_sensor')
        self.forward_right_presence_value = self.devices_value('forward_right_sensor')

    def strategy_1(self):

        """ Seguir em frente até achar o inimigo -> Funcionando

        Estratégia padrão do mini-sumo, ele irá seguir em linha reta até encontrar
        o robo adversário ou encontrar as bordas da arena
        """
        self.update_sensor()

        if self.left_presence_value > 500:
            self.robot.state = 'LEFT'

        elif self.right_presence_value > 500:
            self.robot.state = 'RIGHT'

        elif self.forward_right_presence_value > 500:
            robot.state = 'FORWARD_RIGHT'

        elif self.forward_left_presence_value > 500:
            robot.state = 'FORWARD_LEFT'

        elif self.front_presence_value > 500:
            self.robot.state = 'FORWARD'
            
        elif self.left_line_value > 200 and self.time - self.task_time > self.T:
            self.task_time = self.time
            self.robot.state = 'RIGHT'

        elif self.right_line_value > 200 and self.time - self.task_time > self.T:
            self.task_time = self.time
            self.robot.state = 'LEFT'
        
        elif self.time - self.task_time > self.T:
            self.robot.state = 'FORWARD'
            
            
    def strategy_2(self):
        """
        Brecando até ficar de frente ou encontrar o inimigo -> Funcionando
        """
        
        self.update_sensor()
        
        if self.c == 0:

            if (self.left_line_value < 200 or self.right_line_value < 200) and (self.time - self.task_time > 0.2):
                self.task_time = self.time
                self.robot.state = 'FORWARD'
                
            elif self.front_presence_value > 500:
                self.robot.state = 'VRUM'
            
            elif self.forward_left_presence_value > 500:
                self.robot.state = 'FORWARD_LEFT'
            
            elif self.forward_right_presence_value > 500:
                self.robot.state = 'FORWARD_RIGHT'
                
            elif self.left_presence_value > 500:
                self.robot.state = 'LEFT'
                self.c += 1
                
            elif self.right_presence_value > 500:
                self.robot.state = 'RIGHT'
                self.c += 1
           
            elif self.time - self.task_time < 0.5:
                self.robot.state = 'STOP' 
                
            elif (self.left_line_value < 200 or self.right_line_value < 200):
                self.c += 1
        else:
            self.strategy_1()
            
    def strategy_3(self):
        """
        Zigue-Zague -> não está funcionando direito
        """
    
        self.update_sensor()
  
        if self.c == 0:
            
            if self.left_line_value > 200:
                self.task_time = self.time
                self.robot.state = 'RIGHT'
            elif self.right_line_value > 200:
                self.task_time = self.time
                self.robot.state = 'LEFT'
            # Fica fazendo um zig-zag
            elif self.time - self.task_time > 0.8 and self.robot.state == 'FORWARD_RIGHT':
                self.robot.state = 'FORWARD_LEFT'
                
            elif self.time - self.task_time > 0.8:
                robot.state = 'FORWARD_RIGHT'

            # Quando encontra o outro robo, entra na estrategia de perseguicao
            if self.right_presence_value > 500 or self.left_presence_value > 500 or self.front_presence_value > 500:
                self.task_time = self.time
                self.c += 1
        else:
            self.strategy_1()
            
    def strategy_4(self):
        """
        Trajetória em arco pela direita -> funcionando direito
        """

        self.update_sensor()
        if self.c == 0:
            if self.left_presence_value > 500 or self.left_presence_value > 500 or self.front_presence_value > 500 or self.forward_right_presence_value > 500 or self.forward_left_presence_value > 500:
                self.c += 1
                
            elif self.left_line_value > 200 and self.time - self.task_time > self.T:
                self.robot.wheels_velocity(MAX_SPEED, MAX_SPEED)
                self.task_time = self.time
                self.robot.state = 'RIGHT'
    
            elif self.right_line_value > 200 and self.time - self.task_time > self.T:
                self.robot.wheels_velocity(MAX_SPEED, MAX_SPEED)
                self.task_time = self.time
                self.robot.state = 'LEFT'
            
            elif self.time - self.task_time > self.T:
                self.robot.state = 'ARC_RIGHT'
            
        else: 
            self.strategy_1()
            
    def strategy_5(self):
        """
        Trajetória em arco pela esquerda -> funcionando direito
        """
    
        self.update_sensor()
        
        if self.c == 0:
            if self.left_presence_value > 500 or self.left_presence_value > 500 or self.front_presence_value > 500 or self.forward_right_presence_value > 500 or self.forward_left_presence_value > 500:
                self.c += 1
                
            elif self.left_line_value > 200 and self.time - self.task_time > self.T:
                self.robot.wheels_velocity(MAX_SPEED, MAX_SPEED)
                self.task_time = self.time
                self.robot.state = 'RIGHT'
    
            elif self.right_line_value > 200 and self.time - self.task_time > self.T:
                self.robot.wheels_velocity(MAX_SPEED, MAX_SPEED)
                self.task_time = self.time
                self.robot.state = 'LEFT'
            
            elif self.time - self.task_time > self.T:
                self.robot.state = 'ARC_LEFT'
            
        else: 
            self.strategy_1()
            
        
if __name__ == '__main__':

    robot = stateMachine(Robot())
    robot_strategies = Strategies(robot)

    while robot.robot.step(TIME_STEP) != -1:
        robot_strategies.strategy_4()
        robot.process()
