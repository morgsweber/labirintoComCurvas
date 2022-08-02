# T2 CG 
### Leonardo S. e Morgana Weber

## Controles
* **ESC**: fecha a aplicação
* **ESPAÇO**: para o carro
* **A**: escolhe a próxima curva no sentido antihorário
* **D**: escolhe a próxima curva no sentido horário
* **W**: move o carro para frente, caso ele esteja parado
* **S**: move o carro para trás, caso ele esteja parado

## Modelagem
![img](Architecture.png)
#### Ruas
Para *f(x)* sendo a função de curva bézier, o primeiro ponto é o sentido backward e o último é o sentido foreward, onde *f(x)* = ponto inicial e *f(x)* = ponto final. logo uma velocidade positiva vai do 0 ao 1 e uma negativa do 1 ao 0.

#### Conexões
Cada rua possui duas listas de ruas conectadas, tanto do sentido foreward da curva quando no backward. Como existem casos como o C possuindo a conexão A entre ponto foreward C e foreward A, precisamos de uma maneira de aplicar um viés na rua, multiplicando sua posição e velocidades por -1 caso a conexão não for no sentido convencional (backward para backward e foreward para foreward) 

#### Carro
O carro possui referência para a curva que ele está (`Car.road`), usado para calcular sua posição global e rotação baseado na fração que se encontra da curva (`Car.position`) e uma referência para a próxima curva (`Car.next`), calculado após ultrapassar a metade da curva.

### Colisão
Cada rua tem um Set de carros (`Road.cars`) iminigos presente nela, assim com base no atributo de posição absoluta na curva (`Car.length`), verifica se a distância entre o player e todos os inimigos na curva e pequena o suficiente para ser considerada uma colisão.
