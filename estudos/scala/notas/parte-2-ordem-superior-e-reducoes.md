# Parte 2: funções de ordem superior e reduções

Exercícios correspondentes: 16 a 24 de [`ex_scala.ipynb`](../ex_scala.ipynb).

## 0. `val` fixa a referência, não o conteúdo

```scala
val arr = Array(1, 2, 3)
arr(0) = 99        // permitido: o Array é mutável por dentro
// arr = Array(4)  // erro: não dá para apontar o val para outro objeto
```

Em Scala idiomático evitamos tanto o `var` quanto alterar arrays no lugar: usamos operações como `map`, que criam uma coleção nova.

## 1. Funções são valores e têm tipo

Em Scala, uma função tem um tipo, assim como `Int` ou `String`. O tipo `Double => Double` significa "recebe um `Double` e devolve um `Double`".

```scala
val half: Double => Double = x => x / 2
def applyTwice(f: Double => Double, x: Double): Double = f(f(x))
applyTwice(half, 20.0)   // 5.0
```

Uma **função de ordem superior** é aquela que recebe ou devolve outra função. `map`, `filter` e `foldLeft` são todas assim. Um método `def` também pode ser passado onde se espera uma função: o compilador faz a conversão sozinho.

## 2. A sintaxe curta `_`

Quando o parâmetro de uma lambda aparece **uma única vez**, dá para trocá-lo por `_`:

```scala
values.map(x => x + 1)     // forma completa
values.map(_ + 1)          // forma curta
values.filter(_ >= 0)

values.map(x => x * x)     // aqui não dá: _ * _ significa dois parâmetros diferentes
```

Cada `_` é um parâmetro **novo**: `_ * _` equivale a `(a, b) => a * b`. Se você precisa usar o mesmo valor duas vezes, escreva a lambda completa.

## 3. Lambda com `case` para desmontar tuplas

Muitas operações (`zip`, `zipWithIndex`, `foldLeft` com tupla) trabalham com pares. Dá para desmontar o par direto no parâmetro:

```scala
val people = Array(("Ana", 21), ("Rui", 30))
people.map { case (name, age) => s"$name tem $age anos" }
```

Note as **chaves** `{ case ... }` no lugar dos parênteses. É *pattern matching*, assunto da próxima parte.

## 4. `foldLeft`: a redução sequencial

`foldLeft(valorInicial)((acc, x) => novoAcc)` percorre os elementos da esquerda para a direita e carrega um **acumulador** `acc`. É o equivalente funcional do laço `while` com `var`, só que sem estado mutável.

```scala
Array(2, 3, 4).foldLeft(1)((acc, x) => acc * x)   // 24
```

| passo | `acc` | `x` | novo `acc` |
| --- | --- | --- | --- |
| 1 | 1 | 2 | 2 |
| 2 | 2 | 3 | 6 |
| 3 | 6 | 4 | 24 |

O valor inicial define o **tipo do resultado** e o que sai quando a coleção está vazia. Ele também pode ser uma tupla, para acumular duas coisas numa só passada:

```scala
val (lo, hi) = Array(4.0, -1.0, 7.0).foldLeft((Double.MaxValue, Double.MinValue)) {
  case ((min, max), x) => (math.min(min, x), math.max(max, x))
}
// lo = -1.0, hi = 7.0
```

## 5. `reduce` e por que isso importa no Spark

`reduce(op)` é parecido com o `foldLeft`, mas não tem valor inicial: usa o primeiro elemento. Por isso ele falha em coleção vazia.

A diferença teórica é a seguinte. O `foldLeft` impõe uma ordem estrita, da esquerda para a direita, então é inerentemente **sequencial**. Num `reduce` distribuído, o Spark reduz cada partição separadamente, em paralelo, e depois combina os resultados parciais numa ordem que não é garantida. Isso só dá o resultado certo se a operação for **associativa**:

$$
(a \oplus b) \oplus c = a \oplus (b \oplus c)
$$

- $a$, $b$, $c$ são elementos quaisquer da coleção;
- $\oplus$ é a operação binária passada ao `reduce` (por exemplo, `_ + _`).

Em palavras: o resultado não pode depender de agrupar primeiro os dois elementos da esquerda ou os dois da direita. Como a ordem das partições também não é garantida, a operação precisa ainda ser **comutativa**:

$$
a \oplus b = b \oplus a
$$

Em palavras: trocar a ordem dos dois operandos não muda o resultado.

## 6. Outras operações frequentes

```scala
val xs = Array(5.0, 2.0, 8.0)

Array("a", "b", "c").zip(Array(1, 2, 3))   // Array(("a",1), ("b",2), ("c",3)); corta no menor tamanho
xs.zipWithIndex                            // Array((5.0,0), (2.0,1), (8.0,2)): (elemento, posição)

xs.count(_ > 4)                            // 2: quantos satisfazem a condição
xs.exists(_ > 7)                           // true: pelo menos um satisfaz?
xs.forall(_ > 0)                           // true: todos satisfazem?

xs.min ; xs.max ; xs.sorted                // para tipos que já se comparam sozinhos
val words = Array("spark", "jvm", "scala")
words.minBy(_.length)                      // "jvm": o menor segundo um critério
words.sortBy(_.length)                     // Array("jvm", "spark", "scala")
words.sortBy(w => -w.length).take(1)       // Array("spark"): ordem decrescente e os k primeiros
```

`minBy`, `maxBy` e `sortBy` recebem uma função que extrai a **chave de comparação**. É assim que se ordenam objetos de `case class` por um campo.
