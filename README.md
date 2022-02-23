# Cvraft

Instead of writing your CV or resumé in Microsoft Word, Google Docs, or some proprietary tools, you can just write it in Markdown. As a Markdown file is just plain text, you can easily track version with Git or your VCS of choice. Copy and paste with ease.

**cvraft** transforms your Markdown file to a ready-to-use HTML file. You can also [customize it with ease](#customization).

## Install

```bash
pip install cvraft
```

## Usage

Output HTML file to a **build** directory in current directory. It also copies **static** directory (if it exists in the same directory as the source Markdown file) to **build**.

```bash
cvraft build <path/to/file.md>
```

View the HTML file in a local web server at http://localhost:9000

```bash
cvraft serve
```

## Customization

The different with standard Markdown tool is that the output HTML is tweaked to wrap different parts of your CV in proper **section** tags. This will ease your cutomization with CSS.

The generated HTML structure could look like this

![HTML structure](./docs/images/html-structure.png)

With this structure, you can write your custom CSS in the **static/styles/main.css**. This path is the default CSS path in the generated HTML file.