# equipe_2

## Progresso realizado na programação do webots:


## Considerações importantes sobre o mini-sumô simplificado

    Os motores devem ter uma velocidade de rotação de 50, as vezes o webots pode resetar para 12 automaticamente, então 
    ela deve ser posta manualmente se for o caso essa velocidade toda não é usada normalmente, apenas para fazer
    algumas curvas, já que o bloco resiste muito a rotação.
    
    Os sensores de linha tiveram que fica em uma posição não convencional por não funcionarem quando estavam em baixo do robô
    
    Algumas estratégias que dependiam muito da rotação, que funcionavam no kheperaIII não conseguiram ser convertidas para o 
    robô simplificado
    
    
## Dados obtidos com o kheperaIII:

  #### Sensores infravermelho:
      Possuem o papel de verificar se o robô ainda está sobre a arena de mini-sumo, foi verificado que quando o 
      mesmo está nas bordas brancas da arena os valores obtidos pelos sensores podem ultrapassar a 4000.
  
  ### Sensores ultrassônicos:
      Responsáveis pela localização do oponente e o direcionamento do movimento do robô. Esses sensores na simulação 
      só adquirem valores quando o oponente está muito do mini-sumo, tornando-os inviáveis para uma competição real, 
      contudo na simulação quando eles detectam algo, os valores ultrapassam 1000.
  
  
  ### Trajetória de arco:
  
    Com o motor de fora no máximo RPM, quanto menor a velocidade do motor de dentro, mais fechado é o arco, enquanto 
    quanto maior a velocidade do motor de dentro maior é o arco.
  
    

    

