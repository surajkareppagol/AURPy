# AURPy

`AURPy` is a AUR helper 👨‍🔧 written in python.

## Why one more AUR helper ?

It is just a hobby project, i came across `Aurweb RPC Interface` and wanted to use it, and see if i could create one (AUR Helper).

## How to use it ?

Here `Poetry` is used for dependency management and packaging in Python, install it by visiting  [here](https://python-poetry.org/docs/#:~:text=Poetry%20is%20a%20tool%20for,build%20your%20project%20for%20distribution.).

Next clone this repository,

```bash
git clone https://github.com/surajkareppagol/AURPy
cd AURPy
```

```bash
poetry init
```

```bash
poetry install
```

Once all the dependecies are installed,

```bash
poetry run python src/main.py [Package]
```

![AURPy](https://raw.githubusercontent.com/surajkareppagol/assets-for-projects/main/AURPy/AURPy%20A.png)

> **Warning**: This Is Just An Experimental Project, It Might Be Dangerous, Use It In A Virtual Environment.

`Rich` is used for all the terminal styles.

## Is it usable ?

Yes, but it needs root permissions as `makepkg` can't execute, so be careful here.

For development `Response JSON`,

```json
{
  "resultcount": 2,
  "results": [
    {
      "Description": "Python IDE for beginners",
      "FirstSubmitted": 1472854321,
      "ID": 1371299,
      "LastModified": 1702829671,
      "Maintainer": "tecnotercio",
      "Name": "thonny",
      "NumVotes": 37,
      "OutOfDate": null,
      "PackageBase": "thonny",
      "PackageBaseID": 115205,
      "Popularity": 0.754598,
      "URL": "https://thonny.org",
      "URLPath": "/cgit/aur.git/snapshot/thonny.tar.gz",
      "Version": "4.1.4-1"
    },
    {
      "Description": "Python IDE for beginners.",
      "FirstSubmitted": 1494621443,
      "ID": 1125610,
      "LastModified": 1660397328,
      "Maintainer": "matsjoyce",
      "Name": "thonny-git",
      "NumVotes": 0,
      "OutOfDate": null,
      "PackageBase": "thonny-git",
      "PackageBaseID": 122314,
      "Popularity": 0,
      "URL": "http://thonny.org/",
      "URLPath": "/cgit/aur.git/snapshot/thonny-git.tar.gz",
      "Version": "r3936.c1da4858-1"
    }
  ],
  "type": "search",
  "version": 5
}
```

## What next ?

Need to go thorugh some other popular AUR helpers and need to check how they work behind the scenes and implement those techniques here also. I will be working on it, adding more functionalities.
