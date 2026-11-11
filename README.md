### Hi, I’m Dimitar Anastasov 👋

**Systems programmer working on optimization: Systems for ML and ML for Systems.**

<a href="https://www.linkedin.com/in/dimitar-anastasov-339a94310/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://linkedin.com/company/systems-society-bulgaria"><img src="https://img.shields.io/badge/System_Society_Bulgaria-0A7A5A?style=flat-square&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgMTAwIj48cmVjdCB3aWR0aD0iNzUiIGhlaWdodD0iMjUiIGZpbGw9IiNmZmYiLz48cmVjdCB4PSIyNSIgeT0iMzcuNSIgd2lkdGg9Ijc1IiBoZWlnaHQ9IjI1IiBmaWxsPSIjZmZmIi8%2BPHJlY3QgeT0iNzUiIHdpZHRoPSI3NSIgaGVpZ2h0PSIyNSIgZmlsbD0iI2ZmZiIvPjwvc3ZnPg%3D%3D" alt="System Society Bulgaria"></a>
<a href="https://quicx.dev"><img src="https://img.shields.io/badge/quicx.dev-FF5700?style=flat-square" alt="quicx.dev"></a>

I’m a final-year student at TUES. I like putting low-level knowledge, mathematics and machine learning together to build things that didn’t exist before. Right now I’m writing research papers on ML for Systems and testing the ideas inside my own engine, Quicx.

### What I work on

<table>
<tr>
<td width="50%" valign="top">
<sub><b>01</b>&ensp;ML for Systems</sub>
<h3>A task queue with a hard memory limit</h3>
<p><a href="https://github.com/anastassow/Quicx"><b>Quicx</b></a> is my own task queue engine in C, with its own memory allocator and binary protocol. It gets a memory budget and never goes past it: when memory is full, valuable tasks push out less valuable ones instead of the whole thing crashing.</p>
<p>The program is 36 KB on a Raspberry Pi. Now I’m researching how it can learn by itself which tasks matter.</p>
</td>
<td width="50%" valign="top">
<sub><b>02</b>&ensp;Systems for ML</sub>
<h3>Training neural networks on the CPU</h3>
<p><a href="https://github.com/Molikano/Sandokan"><b>Sandokan</b></a> trains neural networks on the device itself, with no GPU and no Python, for robots and embedded systems that keep learning after they ship.</p>
<p>Its memory comes from <a href="https://github.com/anastassow/PMAD"><b>PMAD</b></a>, my slab allocator in C: one pool reserved at start, every allocation O(1), no system calls on the hot path.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<sub><b>03</b>&ensp;Developer tools</sub>
<h3>Documentation for mainframe code</h3>
<p><a href="https://github.com/IBM-SUMMER-PRACTICE-2026/ZDoc"><b>ZDoc</b></a> reads PL/X, C, C++ and Java and turns the doc comments into browsable Markdown or HTML, like Doxygen for mixed mainframe codebases.</p>
<p>There was no maintained open-source documentation generator for PL/X, so we built one at the IBM summer practice.</p>
</td>
<td width="50%" valign="top">
<sub><b>04</b>&ensp;Compilers and robotics</sub>
<h3>A compiler, and the robot that started Quicx</h3>
<p>I wrote a compiler for a C-style language, and worked on an autonomous robot that finds plant diseases with on-board vision and machine learning.</p>
<p>The model was slower than the cameras, the robot ran out of memory in the middle of a field and stopped. That is the problem Quicx solves.</p>
</td>
</tr>
</table>

### Community

<a href="https://linkedin.com/company/systems-society-bulgaria"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/profile/ssb-dark.png"><img src="assets/profile/ssb-light.png" width="100%" alt="System Society Bulgaria. Founder. Free monthly sessions in Sofia."></picture></a>

I founded System Society Bulgaria for people who want to take systems programming further, into business, ML, reinforcement learning and quantum computing. Follow it on [LinkedIn](https://linkedin.com/company/systems-society-bulgaria) and come to the sessions on [Luma](https://luma.com/systems-society-bulgaria).

### Skills and main technologies

<table>
<tr>
<td valign="top" width="160"><b>Skills</b></td>
<td>
<img src="https://img.shields.io/badge/Mathematics-0A7A5A?style=flat-square" alt="Mathematics">
<img src="https://img.shields.io/badge/Machine_learning-0A7A5A?style=flat-square" alt="Machine learning">
<img src="https://img.shields.io/badge/Optimization-0A7A5A?style=flat-square" alt="Optimization">
<img src="https://img.shields.io/badge/Systems_programming-0A7A5A?style=flat-square" alt="Systems programming">
<img src="https://img.shields.io/badge/Operating_systems-0A7A5A?style=flat-square" alt="Operating systems">
<img src="https://img.shields.io/badge/Microprocessor_architecture-0A7A5A?style=flat-square" alt="Microprocessor architecture">
<img src="https://img.shields.io/badge/Memory_management-0A7A5A?style=flat-square" alt="Memory management">
<img src="https://img.shields.io/badge/Parallel_computing-0A7A5A?style=flat-square" alt="Parallel computing">
</td>
</tr>
<tr>
<td valign="top" width="160"><b>Main technologies</b></td>
<td>
<img src="assets/tech/c.svg" width="48" title="C" alt="C">
<img src="assets/tech/cpp.svg" width="48" title="C++" alt="C++">
<img src="assets/tech/x86.svg" width="48" title="x86 assembly" alt="x86 assembly">
<img src="assets/tech/arm.svg" width="48" title="ARM assembly" alt="ARM assembly">
<img src="assets/tech/bash.svg" width="48" title="Bash" alt="Bash">
<img src="assets/tech/python.svg" width="48" title="Python" alt="Python">
<img src="assets/tech/linux.svg" width="48" title="Linux" alt="Linux">
<img src="assets/tech/macos.svg" width="48" title="macOS" alt="macOS">
<br>
<sub>C, C++, x86 and ARM assembly, Bash, Python, Linux, macOS</sub>
</td>
</tr>
</table>

### Also

Before all this I owned a service company and worked as a product owner. I can build web, mobile and desktop apps and set up infrastructure and networks too. It isn’t my passion anymore, but it comes in handy.

### Let’s connect

**Your network is your net worth.** Connect with me on LinkedIn.

<a href="https://www.linkedin.com/in/dimitar-anastasov-339a94310/"><img src="https://img.shields.io/badge/Connect_on_LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Connect on LinkedIn"></a>
