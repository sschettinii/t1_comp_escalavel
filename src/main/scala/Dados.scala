import scala.io.Source
import scala.collection.mutable.ArrayBuffer

// Esqueleto temporário da função de ler os CSVs gerados pelo download_data.py, e transformar nas features/target pra utilizarmos
// na implementação dos modelos.

// Por hora, ainda só testei pra ROAD 3D, mas as funções de .init e .last vão facilitar demais pra que funcione em ambos os csv,
// agora é só uma questão de implementar a função.

// A função, quando pronta, será mais ou menos assim:
// lerCsv(caminho, n) -> n é o número de linhas que serão lidas, e devolve uma tupla (feature, alvos)
// O tipo da tupla é: (Array[Array[Double]], Array[Double])
// Onde o primeiro item são as features, e o segundo são os targets, na mesma ordem das features

object Dados {
    def main(args: Array[String]) : Unit = {
        val road3d = "data/road_network_3d.csv"
        val sgemm = "data/sgemm_gpu.csv"

        // fromFile retorna um ponteiro pro arquivo aberto, mesma coisa do open do Python
        val sourceroad3d = Source.fromFile(road3d)
        val sourcesgemm = Source.fromFile(sgemm)

        // Pras features, o array buffer (tamanho mutável) precisa conter dentro mais um array (tamanho fixo, o par de features), 
        // já que na hora de adicionar os elementos na iteração, precisa percorrer neles

        val featuresroad3dtemp = ArrayBuffer[Array[Double]]()
        val targetroad3dtemp = ArrayBuffer[Double]()

        for (linha <- sourceroad3d.getLines().drop(1).take(5)) {
            // separa o que antes era uma linha só, em uma lista
            val campos = linha.split(",").toList

            val features = campos.init.map(x => x.toDouble)
            featuresroad3dtemp += features.toArray
            
            val target = campos.last.toDouble
            targetroad3dtemp += target
        }

        // Agora sim, convertendo o que tava em ArrayBuffer (que usei antes só pra deixar o tamanho dele mutável),
        // pra um array fixo que vai ser o que vamos usar em ambos os modelos

        val X_road3d = featuresroad3dtemp.toArray
        val y_road3d = targetroad3dtemp.toArray

        // Validação final pra testar se leu tudo certo mesmo
        println(X_road3d.length)
        println(y_road3d.length)
        println(y_road3d(0))

        sourceroad3d.close()
        sourcesgemm.close()
    }
}

