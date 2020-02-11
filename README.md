## Text
#### Example Upload text
```python
from sixecho import Chain, Text
text1 = Text()
#generate from string
text1.generate(str="textfile")
#generate from file
text1.generate(txtpath="text.txt")
#set common info
common_info = {
    "title": "tear",
    "image_url":
    "https://raw.githubusercontent.com/ianare/exif-samples/master/jpg/Canon_40D.jpg",
    "tags": ["novel"],
    "parent_id":""
}
#set reference in your system
ref_info = {
    "creator": "",
    "ref_creator": "",
    "owner": "",
    "ref_owner": "",
}
#set detail info of the book
detail_info = {
    "isbn": "xadadf",
    "author": "watcharapon",
    "publisher": "watcharapon limit",
    "published_date": 1574142753,
    "language": "th",
    "number_of_pages": "100"
}
#set mdata of the book, free fields
meta = {
"xxx":"zaaa",
"vvv":"xxaadsf"
}

text1.set_meta(meta)
text1.set_common_info(common_info)
text1.set_ref_info(ref_info)
text1.set_detail_info(detail_info)

## Submit to SSC chain
sixEOS = Chain(
    private_key="private key",
    host_url=
    "SSCHOST:PORT")

data5 = sixEOS.push_transaction([{
    "actor": "actor name",
    "permission": "active",
}], text1)



```
