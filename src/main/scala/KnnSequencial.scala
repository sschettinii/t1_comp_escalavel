// Leitura dos arquivos CSV
object KnnSequencial {

    def main(args: Array[String]): Unit = {
        val (x, y) = Dados.lerCsv(Dados.caminhoDataset("road"), 2000)
        println(s"${x.length} pontos; primeiro: (${x(0).mkString(", ")}) -> ${y(0)}")

    //Separar em treino e teste
    val corte = (x.length * 0.8).toInt
    println(s"Corte:$corte")
    val (xTreino, xTeste) = x.splitAt(corte)
    }

}