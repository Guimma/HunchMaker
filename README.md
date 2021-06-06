# HunchMaker
## Descrição
Um script escrito em python para prever resultados de jogos de futebol!  
O objetivo aqui é o de criar um programa de lógica simples, que consiga atingir a maior pontuação possível em um bolão esportivo.  
Código é facilmente adaptável para outras competições. 

## Pontuação
| Tipo de Acerto        | Pontos |
| --------------------- | ------ |
| Placar exato          | 25     |
| Gols do time vencedor | 18     |
| Saldo de gols         | 15     |
| Gols do time perdedor | 12     |
| Acertou o vencedor    | 10     |
| Empate garantido      | 4      |  
  
**Para mais informações consulte o [REGULAMENTO](http://www.maisbolao.com.br/regulamento)*  

## Estratégia
Os testes foram realizados simulando apostas em resultados do jogos do Campeonato Brasileiro de 2020.  
Pelos resultados dos testes, foi decidido utilizar a seguinte estratégia:  
 - Para os primeiros 6 jogos, o número de gols do time no jogo será igual a sua média de gols do ano passado.
 - Para o restante dos jogos, o número de gols do time será equivalente ao arredondameneto da média de gols do time no atual campeonato.

## Dados
Os dados foram obtidos pelo UOL, por meio do link:  
http://jsuol.com.br/c/monaco/utils/gestor/commons.js?callback=simulador_dados_jsonp&file=commons.uol.com.br/sistemas/esporte/modalidades/futebol/campeonatos/dados/{ANO_DO_CAMPEONATO}/{ID_DO_CAMPEONATO}/dados.json
