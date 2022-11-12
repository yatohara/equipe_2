##----------------------NÃO ALTERAR----------------------##
from controller import Robot, Motor, DistanceSensor


TIME_STEP = 32
MAX_SPEED = 12

robot = Robot()

#Definindo os motores
roda_esquerda = robot.getDevice("left wheel motor") #Motor esquerdo
roda_direita = robot.getDevice("right wheel motor") #Motor direito
roda_esquerda.setPosition(float('inf'))
roda_direita.setPosition(float('inf'))
roda_esquerda.setVelocity(0.0)
roda_direita.setVelocity(0.0)

#Definindo os sensores infravermelhos inferiores
infraL = robot.getDevice("ds10") #Sensor infravermelho inferior esquerdo
infraR = robot.getDevice("ds9") #Sensor infravermelho inferior direito
infraL.enable(TIME_STEP)
infraR.enable(TIME_STEP)

#Definindos os sensores ultrassônicos
us01 = robot.getDevice("us1") #Sensor ultrassônico lateral esquerdo
us02 = robot.getDevice("us2") #Sensor ultrassônico fronta
us03 = robot.getDevice("us3") #Sensor ultrassônico lateral direito
us01.enable(TIME_STEP)
us02.enable(TIME_STEP)
us03.enable(TIME_STEP)


right_speed = 0.75 * MAX_SPEED
left_speed = 0.75 * MAX_SPEED

turning = 0
num = 0
esq = 0
straight = 0
dir = 0
right = 0 
left = 0


##-------------------------------------------------------##
while robot.step(TIME_STEP) != -1: #Insira dentro desse laço while o código que rodará continuamente (estilo loop do arduino)
    current_time = robot.getTime()
    infraL_value = infraL.getValue()
    infraR_value = infraR.getValue()
    ultra_direita = us01.getValue()
    ultra_frente = us02.getValue()
    ultra_esquerda = us03.getValue()
        

    if turning != 1:
        if infraL_value > 2000 or infraR_value > 2000:  # verifica se os sensores estão na linha branca
            turning = 1
    
    
    if turning == 0:  # faz o robo andar reto
        roda_esquerda.setVelocity(left_speed)
        roda_direita.setVelocity(right_speed)
            
            
    if turning == 1 and num < 18:  # faz o robo girar, creio que uns 150º
            
        roda_esquerda.setVelocity(left_speed)
        roda_direita.setVelocity(-right_speed)
        num += 1
    else:  # reseta as variaveis de giro e angulacao
         num = 0
         turning = 0
         
         
    if left != 1:  # faz com que o robo vire para a esquerda se o sensor detectar algo
        if ultra_esquerda > 1000:
            left = 1  # foi necessario outra variavel de controle, pois quando eu tentei usar a mesma o robo viro uma beyblade
     
    if left == 1 and esq < 5:  # faz o robo girar so um pouco, para que ele fique de frente com o outro
        roda_esquerda.setVelocity(left_speed)
        roda_direita.setVelocity(-right_speed)
        esq += 1
    else:  # reseta a variavel de giro e angulacao
        esq = 0
        left = 0
        
    
    if right != 1:  # é um movimento espelhado do giro para a esquerda
        if ultra_direita > 1000:
            right = 1
     
    if right == 1 and dir < 5:
        roda_esquerda.setVelocity(-left_speed)
        roda_direita.setVelocity(right_speed)
        dir += 1
    else:
        dir = 0
        right = 0
      
    pass
