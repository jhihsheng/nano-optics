# Making Meep codes in a module way
Frequenctly, when writing a simulation scripts, there are many parameters to be explored. One can play around the parameters in one single file. However, it is easy to overwrite some important results when changing parameters. Thus, another way is to save one file for one parameter. But, it results in large amount of files which are hard to track.  The idea here is to make a code into many modules, and  when writnging a simulation scrpit, one can flexibly include the needed modules.

modules fall into 
- cell 
- geometry and material 
- source  

```
For now, I will make these modules as scripts. That is, load these module by excute scripts.
Although using **exec(open('file.py').read())** may be buggy, it seems an easier way than using typical python module.
```
- To avoid complicated argument passing
- To use the same structure in many simulations


