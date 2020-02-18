# Reverse GeoCoder
## What is it?
国勢調査の境界ポリゴンを利用してリバースジオコードが引けるAPIです。

# How do we start the API server?
Docker Composeで起動してください。8000番ポートを使うので、事前に使われていないことを確認してください。

```bash
$ docker-compose build
$ docker-compose up -d
```

次にポリゴンデータをインポートします。同階層に `shapes` ディレクトリを作り、その中に一連のshapeファイルを入れてください。サブディレクトリがあっても大丈夫です。
境界ポリゴンは[e-Stat](https://www.e-stat.go.jp/gis/statmap-search?page=1&type=2&aggregateUnitForBoundary=A&toukeiCode=00200521&toukeiYear=2015&serveyId=A002005212015&coordsys=1&format=shape)からダウンロードしてください。国勢調査の小地域で世界測地系緯度経度のshapeファイルをダウンロードするようにしてください。

格納し終わったら `initializer` を実行します。コマンドの最終引数がshapeファイルが格納されているディレクトリへの相対パスです.

```bash
$ docker-compose exec api python -m reverse_geocoder.initializer ./shapes
```

# How do we send a reverse geocode request?
curlでの例です。

```bash
$ curl -H 'Content-Type:application/json' -d '{"lat": 35.6065536, "lon": 140.1035262}' http://localhost:8000/reverse_geocode
```

# LICENSE
MITです。
