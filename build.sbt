name := "t1-comp-escalavel"
version := "1.0"
scalaVersion := "2.13.18"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "4.2.0"

fork := true
javaOptions += "-Xmx4g"