# CodeWars 刷题

## Replace With Alphabet Position ##

you are required to, given a string, replace every letter with its position in the alphabet.

If anything in the text isn't a letter, ignore it and don't return it.

a being 1, b being 2, etc.

As an example:

>  alphabet_position("The sunset sets at twelve o' clock.")
Should return "20 8 5 19 21 14 19 5 20 19 5 20 19 1 20 20 23 5 12 22 5 15 3 12 15 3 11" as a string.

The answer is :

```
def alphabet_position(text):
    return ' '.join(str(ord(c) - 96) for c in text.lower() if c.isalpha())
```
> 使用asci码获取每个字母的index，然后通过isalpha()判断是否为一个英文字符，并且通过lower()将每个字符转换为小写。
