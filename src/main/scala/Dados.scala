import scala.io.Source
import scala.collection.mutable.ArrayBuffer
import scala.util.Random

// Leitura inicial dos CSVs gerados pelo download_data.py.
// Transforma cada arquivo em (features, alvos) pra usarmos na implementação dos modelos.
//
// Os dois CSVs têm o mesmo formato: cabeçalho na primeira linha, features em todas as colunas
// menos a última, e o alvo na última coluna. Por isso a mesma função serve pros dois datasets.
//
// Tipo do retorno: (Array[Array[Double]], Array[Double])
// O primeiro item são as features, e o segundo são os alvos, na mesma ordem das features.
//
// Esta parte (leitura inicial dos arquivos) foi feita com ajuda de IA generativa,
// o que é permitido pelas regras do trabalho.

object Dados {

    val caminhoRoad3d = "data/road_network_3d.csv"
    val caminhoSgemm = "data/sgemm_gpu.csv"

    // Traduz o nome curto usado na linha de comando ("road" ou "sgemm") pro caminho do CSV
    def caminhoDataset(nome: String): String = nome.toLowerCase match {
        case "road" | "road3d" => caminhoRoad3d
        case "sgemm" => caminhoSgemm
        case outro => throw new IllegalArgumentException(
            s"Dataset desconhecido: '$outro'. Use 'road' ou 'sgemm'.")
    }

    // Lê n linhas do CSV (n <= 0 lê o arquivo inteiro).
    //
    // embaralhar = true sorteia as n linhas do arquivo todo, com semente fixa pra ser reproduzível.
    // Isso importa porque os arquivos estão ordenados: o Road 3D vem agrupado por estrada e o SGEMM
    // por configuração, então pegar só as primeiras n linhas daria uma amostra viciada.
    // Com a mesma semente, os dois algoritmos recebem exatamente os mesmos pontos.
    def lerCsv(caminho: String, n: Int, embaralhar: Boolean = true, semente: Long = 42L)
        : (Array[Array[Double]], Array[Double]) = {

        val source = Source.fromFile(caminho, "UTF-8")

        val features = ArrayBuffer[Array[Double]]()
        val alvos = ArrayBuffer[Double]()

        try {
            // Se não for embaralhar, já dá pra parar de ler depois de n linhas
            val linhas = source.getLines().drop(1).filter(_.trim.nonEmpty)
            val linhasLidas = if (!embaralhar && n > 0) linhas.take(n) else linhas

            for (linha <- linhasLidas) {
                // separa o que antes era uma linha só, em um array de campos
                val campos = linha.split(",")

                features += campos.init.map(x => x.trim.toDouble)
                alvos += campos.last.trim.toDouble
            }
        } finally {
            source.close()
        }

        if (n > features.length) {
            throw new IllegalArgumentException(
                s"Pedido de $n linhas, mas $caminho só tem ${features.length}.")
        }

        // Convertendo o que tava em ArrayBuffer pra arrays fixos, que é o que os modelos usam
        val X = features.toArray
        val y = alvos.toArray

        if (!embaralhar || n <= 0) {
            (X, y)
        } else {
            // Sorteia os índices uma vez só, pra features e alvos continuarem pareados
            val indices = new Random(semente).shuffle(X.indices.toVector).take(n).toArray
            (indices.map(i => X(i)), indices.map(i => y(i)))
        }
    }

    // Validação rápida da leitura: sbt "runMain Dados"
    def main(args: Array[String]): Unit = {
        for (nome <- Seq("road", "sgemm")) {
            val (x, y) = lerCsv(caminhoDataset(nome), 10000)
            println(s"$nome: ${x.length} linhas, ${x(0).length} features, primeiro alvo = ${y(0)}")
        }
    }
}
