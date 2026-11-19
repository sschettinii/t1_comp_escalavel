import org.apache.spark.sql.{DataFrame, SparkSession}

class Bootstrap {
  // Returns a bootstrapped DataFrame
  def exec(X: DataFrame, frac: Double, seed: Int): DataFrame = {
    //Checking requirements for bootstrap execution
    require(X.count() > 0, "Dataframe cannot be empty")
    require(frac >= 0 && frac <= 1, "Fraction must be a number between 0 and 1")

    //Returns bootstrapped df
    X.sample(withReplacement = true, fraction = frac, seed = seed.toLong)
  }
}

//Uncomment for testing
/*
object BootstrapTest {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder().appName("BootstrapTest").master("local[*]").getOrCreate()

    val df = spark.read
      .option("header", "true")
      .option("inferSchema", "true")
      .csv("data/sgemm_gpu.csv")

    val bdf = new Bootstrap().exec(df, 0.3, 1)
    println(bdf.count())

    spark.stop()
  }
}
*/