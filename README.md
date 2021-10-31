Tasks

-- Rua --
* [leo] [done] Ler arquivo de definição de curvas
* [morg] Instanciar ruas com base no arquivo de curvas
* [morg] Obter bounding box de curva bezier (não é tão simples como no políono) e calcular o máximo e mínimo para dar um tamanho para tela
* [morg] Estrutura de ruas no arquivo para conter 20 ruas, sendo 8 bifurcações, 8 trifurcações e o resto de conexões + ou - né, não precisa ser tão louco nisso

-- Carro --
* [leo] [done] Modelar classe carro com curva que ele se encontra, posição na curva, direção (do primeiro ponto ao último ou ao contrário, podemos chamar de cima baixo) e tipo do carro (player ou I.A)
* [leo] [active] Método para desenhar o carro (pensei em ser um triagulo simples), o carro se encontra no ponto x da curva com a rotação na tangente da curva (mds que complicado, acho que precisa derivar) e apontando para direção y
* [leo] [done] Método para o carro se mover, em velocidade constante podendo ir para frente ou para tras, sincronizando a sua  dreção
* [leo] [done] Decisão de próxima curva, é aleatório e é decidido ao carro chegar no meio da curva, precisando de mais um método para definir o que é o meio da curva e ao ter a curva decidida, pintar ela caso for o carro do jogador
* [leo] Controles de usuário, espaço para parar e mover, outra tecla para trocar de curva escolhida