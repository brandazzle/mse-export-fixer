# mse-export-fixer

A command-line app for fixing the `.xml` files generated by the Magic Set Editor Cockatrice exporter. Written in Python 3.7.7.

Install using `pip install mse-export-fixer` and run at the command line using `fixer /path/to/setfile.xml`.
Use the `-h` or `--help` flags to see all options, including custom output file naming, verbose running, automatic datestamping, etc.

In the image URL template, `$name` will be replaced by the card name with all special characters besides hyphens removed and all spaces replaced with `%20`.

By way of background: the current version MSE Cockatrice export template "Cockatrice Exporter ReUpdated" has many issues, some worse than others. 
1. The main issue (which I'm pretty sure causes most of the improper or missing tag issues) is that it still uses the old (v3) Cockatrice set formatting. Among other things, this makes it more likely that Cockatrice reads the `.xml` incorrectly.
2. It doesn't export DFCs (double-faced cards) the way Cockatrice expects them, which is as two separate cards connected using the `<related>` tag, one with the tag `<side>front</side>` and the other with the tag `<side>back</side>`.
3. It doesn't use the `<related>` tag to link cards that create tokens to the predefined tokens they create.
4. It doesn't add rarity information.
5. It adds converted mana costs (the `<cmc>` tag) inconsistently, if at all.
6. Because (I think) of the use of the v3 formatting, it uses the `<color>` tag instead of `<colors>`, and consequently does not properly tag the card colors of hybrid and multicolored cards.
7. It doesn't add color identity (the `<coloridentity>` tag).
8. It doesn't add card numbering within a set (the `num` option within the `<set ... >` tag of a card).
9. It doesn't properly recognize custom emblems.
10. It doesn't add planeswalker rules text (including any nonloyalty abilities), it just puts the ability costs.

Of these issues, the app currently fixes 1, 2, 5, 6, and 9. Rarities and numbering are totally absent from the files that MSE generates, and parsing token names from rules text is hard. I'll work the latter out when I can actually be arsed to do it. Probably.

Note: You'll need to split the card images for the two sides of DFCs yourself, since MSE normally exports them as one file. Just be sure to name the images according to the names of the respective sides and put them in with the rest of your card images, and you should be good.

I'm writing this because I can't find the actual source code for the exporter and can't decompile the `.exe`. 
If anyone can point me to the source, I'd be happy to fix the exporter itself instead.
