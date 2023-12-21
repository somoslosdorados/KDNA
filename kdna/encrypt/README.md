# Documentation - encryption library
## How to create a backup ??
### Not encrypted
```python
from encrypt import encrypt

encrypt.backup("<the path to the folder you wanna save>", "<the name of the backup>", "<path-to-the-place-where-to-create-the-backup>, False")

encrypt.backup("<path-to-your-backup>.tar.gz", "<path-to-restore-your-backup>")
```

### Encrypted
```python
from encrypt import encrypt

encrypt.backup("<the path to the folder you wanna save>", "<the name of the backup>", "<path-to-the-place-where-to-create-the-backup>, True")

encrypt.backup("<path-to-your-backup>.enc", "<path-to-restore-your-backup>")
```

### Example of a saved backup and then restored
```python
encrypt.backup("../neovim-darker", "yolo_encrypted", ".", True)
encrypt.restore("yolo_encrypted.enc", "yolo_decrypted")
```
