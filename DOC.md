# <span style="color: MediumSpringGreen">SQLite との違い</span>

## <span style="color: DarkTurquoise">1.</span> primary-key に null または、None の代入ができない。

Column()のインスタンス化時に primary_key=True ならば、自動的に unique=True not_null=True に変更しています。

-   理由としては、Primary Key に Null を重複して挿入できるというのが SQLite 自信のバグであるため、SQLite のバグをけすため。

## <span style="color: DarkTurquoise">2.</span> Blob/Byte のデータのデフォルト設定が出来ません。

調べるのめんどかった。
あとデフォルト設定できると、データインサート時に DB ファイル肥大化が恐れられる。
