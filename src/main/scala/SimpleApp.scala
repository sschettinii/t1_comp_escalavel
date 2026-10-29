/* SimpleApp.scala, utilizei o próprio exemplo da documentação do Apache Spark com Scala para um teste inicial. Podemos 
só apagar isso no futuro, mas serve pra indicar que é o setup do Scala + Apache Spark */

import org.apache.spark.sql.SparkSession

object SimpleApp {
  def main(args: Array[String]): Unit = {
    val logFile = "readme.md" // Should be some file on your system
    val spark = SparkSession.builder.master("local[*]").appName("Simple Application").getOrCreate()
    val logData = spark.read.textFile(logFile).cache()
    val numAs = logData.filter(line => line.contains("a")).count()
    val numBs = logData.filter(line => line.contains("b")).count()
    println(s"Lines with a: $numAs, Lines with b: $numBs")
    spark.stop()
  }
}