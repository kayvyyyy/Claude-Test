#!/usr/bin/env python3
"""
Generate 'AI Engineer in 1 Year' PDF.
Uses Arial from Windows Fonts for Unicode support.
All multi_cell calls pass explicit widths to avoid layout issues.
"""

from fpdf import FPDF
import datetime
import os

# -- colour palette -----------------------------------------------------------
BLUE      = (41, 98, 255)
DARK_BLUE = (20, 50, 140)
LIGHT_BG  = (235, 241, 255)
WHITE     = (255, 255, 255)
BLACK     = (30, 30, 30)
GRAY      = (100, 100, 100)
GREEN_BG  = (230, 245, 230)
ACCENT    = (0, 200, 150)

FONT_DIR = r"C:\Windows\Fonts"
REGULAR   = os.path.join(FONT_DIR, "arial.ttf")
BOLD      = os.path.join(FONT_DIR, "arialbd.ttf")
ITALIC    = os.path.join(FONT_DIR, "ariali.ttf")
BOLD_ITAL = os.path.join(FONT_DIR, "arialbi.ttf")


class RoadmapPDF(FPDF):
    """Custom PDF with Unicode font support and header/footer."""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=22)
        self.add_font("Arial", "", REGULAR)
        self.add_font("Arial", "B", BOLD)
        self.add_font("Arial", "I", ITALIC)
        self.add_font("Arial", "BI", BOLD_ITAL)
        self._lm = 12  # left margin
        self._rm = 12  # right margin

    def _pw(self):
        """Full printable width from current x position to right margin."""
        return self.w - self._rm - self.get_x()

    def _full_w(self):
        """Full page printable width (left margin to right margin)."""
        return self.w - self._lm - self._rm

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Arial", "I", 9)
        self.set_text_color(*GRAY)
        self.cell(0, 8, "AI Engineer Roadmap", align="L")
        self.cell(0, 8, f"Page {self.page_no()}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(10, 14, 200, 14)
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Generated on {datetime.date.today().strftime('%B %d, %Y')}", align="C")

    # -- text helpers --------------------------------------------------------
    def section_title(self, num, title):
        self.set_font("Arial", "B", 16)
        self.set_text_color(*DARK_BLUE)
        self.ln(4)
        self.cell(0, 10, f"{num}.  {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self._lm, self.get_y(), self.w - self._rm, self.get_y())
        self.ln(4)

    def sub_title(self, title):
        self.set_font("Arial", "B", 13)
        self.set_text_color(*BLUE)
        self.set_x(self._lm)
        self.ln(2)
        self.multi_cell(self._full_w(), 8, title)
        self.ln(1)

    def body_text(self, txt):
        self.set_font("Arial", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(self._lm)
        self.multi_cell(self._full_w(), 5.5, txt)
        self.ln(1)

    def bullet(self, txt, indent=15):
        """Indented bullet point."""
        self.set_font("Arial", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(self._lm + indent)
        bullet_w = self.get_string_width("\u2022  ")
        self.cell(bullet_w, 5.5, "\u2022  ")
        remaining = self.w - self._rm - self.get_x()
        self.multi_cell(remaining, 5.5, txt)
        self.set_x(self._lm)

    def highlight_box(self, title, body):
        self.set_fill_color(*LIGHT_BG)
        self.set_draw_color(*BLUE)
        y_start = self.get_y()
        self.set_font("Arial", "B", 10)
        self.set_text_color(*DARK_BLUE)
        self.set_x(self._lm)
        self.cell(self._full_w(), 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_x(self._lm + 2)
        self.set_font("Arial", "", 10)
        self.set_text_color(*BLACK)
        self.multi_cell(self._full_w() - 4, 5.5, body, fill=True)
        self.ln(2)

    def checklist_item(self, text, checked=False):
        box = "[x]" if checked else "[ ]"
        self.set_font("Courier", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(self._lm)
        box_w = self.get_string_width(box) + 2
        self.cell(box_w, 5.5, box)
        self.set_font("Arial", "", 10)
        remaining = self.w - self._rm - self.get_x()
        self.multi_cell(remaining, 5.5, text)
        self.set_x(self._lm)

    def colored_bar(self, label, pct, color=BLUE):
        """Draw a horizontal progress bar at current x position."""
        bar_w = 120
        self.set_font("Arial", "B", 9)
        self.set_text_color(*BLACK)
        self.cell(50, 6, label)
        x = self.get_x()
        y = self.get_y()
        self.set_fill_color(220, 220, 220)
        self.rect(x, y, bar_w, 6, "F")
        self.set_fill_color(*color)
        self.rect(x, y, int(bar_w * pct / 100), 6, "F")
        self.set_xy(x + bar_w + 2, y)
        self.cell(0, 6, f"{pct}%", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def mini_project_box(self, steps):
        self.set_fill_color(*LIGHT_BG)
        self.set_font("Arial", "", 10)
        self.set_text_color(*BLACK)
        self.set_x(self._lm)
        for s in steps:
            self.set_x(self._lm + 8)
            step_w = self._full_w() - 8
            self.multi_cell(step_w, 5.5, f"  {s}", fill=True)
            self.ln(1)
        self.ln(2)

    def resources_block(self, items):
        for title, desc in items:
            self.set_font("Arial", "B", 10)
            self.set_text_color(*DARK_BLUE)
            self.set_x(self._lm)
            self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
            self.set_font("Arial", "", 10)
            self.set_text_color(*BLACK)
            self.set_x(self._lm)
            self.multi_cell(self._full_w(), 5.5, desc)
            self.ln(2)

    def milestone_row(self, m, desc):
        self.set_font("Arial", "B", 10)
        self.set_text_color(*DARK_BLUE)
        self.set_x(self._lm)
        self.cell(22, 6, m + ":")
        self.set_font("Arial", "", 10)
        self.set_text_color(*BLACK)
        remaining = self.w - self._rm - self.get_x()
        self.multi_cell(remaining, 6, desc)
        self.set_x(self._lm)
        self.ln(1)


def build():
    pdf = RoadmapPDF()
    pdf.set_margin(pdf._lm)

    # ==================================================================
    #  TITLE PAGE
    # ==================================================================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Arial", "B", 32)
    pdf.set_text_color(*DARK_BLUE)
    pdf.cell(0, 14, "AI Engineer", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, "in 1 Year", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Arial", "", 16)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 10, "A Complete Step-by-Step Roadmap", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    bars = [
        ("Months 1-3   -- Foundations", 25, BLUE),
        ("Months 4-6   -- Core ML",      50, BLUE),
        ("Months 7-9   -- Specialize",   75, (0, 160, 200)),
        ("Months 10-12 -- Ship It",     100, ACCENT),
    ]
    for lbl, pct, col in bars:
        pdf.set_x(45)
        pdf.colored_bar(lbl, pct, col)

    pdf.ln(8)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(0, 6, "Designed for beginners  |  Python-starting  |  Project-first approach",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Generated: {datetime.date.today().strftime('%B %d, %Y')}",
             align="C", new_x="LMARGIN", new_y="NEXT")

    # ==================================================================
    #  TABLE OF CONTENTS
    # ==================================================================
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.set_text_color(*DARK_BLUE)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    toc = [
        ("1",   "The Big Picture -- What Is an AI Engineer?"),
        ("2",   "Months 1-3: Foundations (Power-Up Phase)"),
        ("2.1", "  Python You Already Need"),
        ("2.2", "  The Tool Stack -- numpy, pandas, matplotlib"),
        ("2.3", "  Just-Enough Math for AI"),
        ("2.4", "  Mini-Project: Linear Regression from Scratch"),
        ("3",   "Months 4-6: Core Machine Learning"),
        ("3.1", "  Classical ML with scikit-learn"),
        ("3.2", "  Deep Learning Foundations with PyTorch"),
        ("3.3", "  MLOps Basics"),
        ("3.4", "  Mini-Project: Cat vs Dog Classifier"),
        ("4",   "Months 7-9: Specialize & Level Up"),
        ("4.1", "  Track A -- NLP / LLMs (Recommended)"),
        ("4.2", "  Track B -- Computer Vision"),
        ("4.3", "  Track C -- ML Platform / Infra"),
        ("5",   "Months 10-12: Production & Portfolio"),
        ("5.1", "  Docker, CI/CD, Model Serving"),
        ("5.2", "  Monitoring & Evaluation"),
        ("5.3", "  Portfolio Projects That Stand Out"),
        ("6",   "Resources & Links"),
        ("7",   "Weekly Action Plan"),
        ("8",   "The Secret Sauce"),
    ]
    for num, title in toc:
        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(*BLACK)
        indent = 6 if "." in num else 0
        pdf.set_x(14 + indent)
        pdf.cell(10, 6, num)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # ==================================================================
    #  1 - THE BIG PICTURE
    # ==================================================================
    pdf.add_page()
    pdf.section_title("1", "The Big Picture -- What Is an AI Engineer?")
    pdf.body_text(
        "An AI engineer is someone who teaches computers to learn on their own. Instead of "
        "writing step-by-step instructions (\"if the button is red, click it\"), you feed the "
        "computer thousands of examples and let it figure out the pattern itself."
    )
    pdf.body_text(
        "Think of it like teaching a child to recognise cats: you don't explain whiskers and "
        "fur patterns -- you just show them lots of cats (and non-cats) until they get it."
    )
    pdf.sub_title("What you will be able to do in 12 months")
    for s in [
        "Write Python that cleans, explores, and visualises real-world data.",
        "Train a model to predict prices, classify images, or understand text.",
        "Deploy that model so other people (or apps) can use it over the web.",
        "Know when AI is the wrong tool -- and reach for a simple rule instead.",
        "Read a research paper and understand enough to try the idea yourself.",
        "Debug a training pipeline when the loss isn't going down.",
    ]:
        pdf.bullet(s)
    pdf.highlight_box(
        "The Mindset Shift",
        "Normal code is deterministic: same input = same output. AI code is statistical: "
        "you give it examples, it finds patterns, and it gets better over time. This changes "
        "everything about how you debug, test, and trust your code."
    )

    # ==================================================================
    #  2 - MONTHS 1-3: FOUNDATIONS
    # ==================================================================
    pdf.add_page()
    pdf.section_title("2", "Months 1-3 -- Foundations (Power-Up Phase)")
    pdf.body_text(
        "You already know Python basics and how to write tests. Now we layer on the specific "
        "tools and concepts you will use every single day as an AI engineer."
    )

    pdf.sub_title("2.1  Python You Already Need")
    pdf.body_text(
        "Beyond basic Python, make sure you are comfortable with these -- they show up "
        "constantly in AI code:"
    )
    for i in [
        "List/dict comprehensions -- cleaner than raw loops",
        "Generator expressions -- memory-efficient iteration over huge datasets",
        "lambda, map, filter, functools.partial",
        "Decorators -- used by Flask, PyTorch, and many ML frameworks",
        "Context managers (with open(...) as f:)",
        "'*args' and '**kwargs' -- you will see these in every library",
        "Type hints -- you already use them; they keep ML code maintainable",
        "Virtual environments (venv / conda) -- isolate your project dependencies",
    ]:
        pdf.checklist_item(i, checked=True)
    pdf.ln(4)

    pdf.sub_title("2.2  The Tool Stack -- numpy, pandas, matplotlib")
    pdf.body_text(
        "These three libraries are the Python data stack. Learn them early because every ML "
        "library sits on top of them."
    )
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.set_x(pdf._lm)
    pdf.cell(0, 6, "numpy", new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "NumPy gives you arrays that are 10-100x faster than Python lists. You will use it for "
        "all math: matrix multiplication, random numbers, statistical summaries, reshaping data. "
        "Learn: array creation, broadcasting, indexing/slicing, np.dot, np.random."
    )
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.set_x(pdf._lm)
    pdf.cell(0, 6, "pandas", new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "Pandas is a spreadsheet inside Python. Real-world data is messy. Pandas helps you load, "
        "clean, filter, group, and merge it. Learn: DataFrame, Series, read_csv, groupby, "
        "fillna, apply, merge, pivot_table."
    )
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*BLUE)
    pdf.set_x(pdf._lm)
    pdf.cell(0, 6, "matplotlib + seaborn", new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "You cannot improve what you cannot see. Visualising data reveals patterns, outliers, "
        "and bugs. Learn: line plots, scatter plots, histograms, heatmaps, subplots. Seaborn "
        "makes pretty charts in 1 line."
    )

    pdf.add_page()
    pdf.sub_title("2.3  Just-Enough Math for AI")
    pdf.body_text(
        "You do NOT need a math degree. You need enough to read a blog post and not panic. "
        "Here is the minimum:"
    )
    for title, desc in [
        ("Vectors",
         "Ordered lists of numbers [x, y, z]. A cat picture is a vector of 3072 numbers "
         "(32x32 pixels x 3 colours)."),
        ("Matrices",
         "Tables of numbers. Matrix multiplication = the engine under every neural network."),
        ("Derivatives",
         "\"If I nudge this dial, how much does the output change?\" -- the core of learning."),
        ("Gradients",
         "A list of derivatives for every dial. Gradient descent = turn all the dials to make "
         "the answer less wrong."),
        ("Probability",
         "How likely is something? 90% confidence = the model is pretty sure. Essential for "
         "understanding predictions and uncertainty."),
    ]:
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(*BLACK)
        pdf.set_x(pdf._lm)
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.body_text(desc)
        pdf.ln(1)

    pdf.highlight_box(
        "Resources for Math",
        "3Blue1Brown -- Essence of Linear Algebra + Calculus (YouTube, ~4h total). "
        "Khan Academy -- probability & statistics (start at 'Basic probability'). "
        "StatQuest -- short, funny explanations of ML concepts."
    )

    pdf.sub_title("2.4  Mini-Project: Linear Regression from Scratch")
    pdf.body_text(
        "This is your first real ML project. Write it in pure Python + numpy, NO libraries. "
        "You will:"
    )
    pdf.mini_project_box([
        "Generate fake data: y = 2x + 1 + some random noise",
        "Write a prediction function: y_pred = w * x + b",
        "Write a loss function: mean squared error",
        "Compute gradients manually (or approximate them)",
        "Write a gradient descent loop that updates w and b",
        "Watch the loss go down and the line fit the data",
        "Celebrate -- you just wrote a learning algorithm!",
    ])

    # ==================================================================
    #  3 - MONTHS 4-6: CORE ML
    # ==================================================================
    pdf.add_page()
    pdf.section_title("3", "Months 4-6 -- Core Machine Learning")

    pdf.sub_title("3.1  Classical ML with scikit-learn")
    pdf.body_text(
        "Before deep learning, there was (and still is) 'classical' ML. These algorithms are "
        "simple, fast, and work well on tabular data (spreadsheets). Most business problems "
        "are solved with these, not neural networks."
    )
    for a in [
        "Linear / Logistic Regression -- predict a number or a yes/no",
        "Decision Trees & Random Forests -- the 'wisdom of the crowd' for tabular data",
        "SVM -- finds the best dividing line between two classes",
        "K-Nearest Neighbours -- look at the closest examples and vote",
        "K-Means clustering -- group similar things together with no labels",
        "PCA -- shrink 1000 columns down to 2 for visualisation",
    ]:
        pdf.bullet(a)
    pdf.body_text(
        "Learn the scikit-learn Pipeline API -- it chains preprocessing + model + prediction "
        "into one object. This is what production code looks like."
    )
    pdf.body_text(
        "Critical concepts that apply everywhere: overfitting (memorising instead of learning), "
        "train/test split, cross-validation, bias-variance tradeoff, regularisation (L1/L2), "
        "evaluation metrics (accuracy, precision, recall, F1, ROC-AUC)."
    )

    pdf.sub_title("3.2  Deep Learning Foundations with PyTorch")
    pdf.body_text(
        "PyTorch is the most popular deep learning framework. It does ONE magical thing: "
        "it tracks every calculation so it can automatically compute gradients "
        "(remember derivatives? autograd does them for you)."
    )
    pdf.body_text("Build up step by step:")
    for s in [
        "Tensors -- numpy arrays that live on the GPU",
        "Autograd -- automatic gradient calculation",
        "nn.Module -- build your own neural network by stacking layers",
        "DataLoader -- load data in batches without writing a loop yourself",
        "Training loop -- forward pass, loss, backward(), optimizer.step()",
        "Move to GPU with .to('cuda') -- watch it go 10x faster",
    ]:
        pdf.checklist_item(s)
    pdf.ln(2)
    pdf.highlight_box(
        "The 50-line Rule",
        "A standard image classifier (CIFAR-10) is about 50 lines of PyTorch. "
        "If your code is longer than that, you are probably overcomplicating it."
    )

    pdf.sub_title("3.3  MLOps Basics")
    pdf.body_text(
        "MLOps = making ML work in the real world, not just on your laptop. Start with:"
    )
    for o in [
        "Experiment tracking -- Weights & Biases or MLflow (log every run, compare results)",
        "Model serialisation -- torch.save / torch.load, ONNX export",
        "Simple serving -- FastAPI endpoint that loads a model and returns predictions",
        "Config files -- YAML configs so you never hardcode hyperparameters",
    ]:
        pdf.bullet(o)

    pdf.sub_title("3.4  Mini-Project: Cat vs Dog Classifier")
    pdf.body_text(
        "Your first 'real' deep learning project. Use a dataset of 25,000 cat & dog images. "
        "You will learn about data loading, image transforms, convolutional layers, "
        "transfer learning (using a pretrained model), and avoiding overfitting."
    )

    # ==================================================================
    #  4 - MONTHS 7-9: SPECIALISE
    # ==================================================================
    pdf.add_page()
    pdf.section_title("4", "Months 7-9 -- Specialise & Level Up")
    pdf.body_text(
        "Now you pick a direction. All three tracks lead to a career, but they aim at "
        "different kinds of roles. Pick the one that excites you most."
    )
    pdf.ln(2)

    # TRACK A
    pdf.sub_title("4.1  TRACK A -- NLP / LLMs (Recommended)")
    pdf.set_fill_color(*GREEN_BG)
    pdf.set_text_color(*BLACK)
    pdf.set_font("Arial", "B", 10)
    pdf.set_x(pdf._lm)
    pdf.cell(pdf._full_w(), 7, "  Why this track?", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.body_text(
        "LLMs are the hottest area in AI right now. Every company wants to build chatbots, "
        "summarisation tools, code assistants, and knowledge retrieval systems. Demand vastly "
        "outpaces supply."
    )
    pdf.body_text("Core topics to learn:")
    for t in [
        "Transformer architecture -- how 'Attention Is All You Need' works",
        "Tokenisation -- how text becomes numbers (and why it matters)",
        "Pretrained models -- downloading GPT, Llama, Mistral from Hugging Face",
        "RAG (Retrieval-Augmented Generation) -- chatbot that looks things up before speaking",
        "Vector databases -- Chroma, Pinecone, Qdrant -- store embeddings for fast search",
        "Fine-tuning -- LoRA / QLoRA -- adapt a big model cheaply",
        "Prompt engineering -- get better answers by asking better questions",
        "Agents -- LangGraph, CrewAI -- models that use tools and take actions",
        "Evaluation -- RAGAS, LLM-as-judge -- is your chatbot actually good?",
    ]:
        pdf.bullet(t)
    pdf.highlight_box(
        "Key Libraries",
        "transformers (Hugging Face), langchain, llama-index, chromadb, vllm, ollama, pytorch"
    )

    # TRACK B
    pdf.add_page()
    pdf.sub_title("4.2  TRACK B -- Computer Vision")
    pdf.body_text(
        "If you are fascinated by cameras, self-driving cars, medical imaging, or augmented "
        "reality, vision is your track."
    )
    for t in [
        "CNNs -- convolutions, pooling, strides, receptive fields",
        "Popular architectures -- ResNet, EfficientNet, YOLO",
        "Object detection -- finding and bounding-boxing objects in images",
        "Segmentation -- pixel-level classification (e.g. every pixel = road, car, sky)",
        "Image generation -- GANs, Diffusion models (Stable Diffusion)",
        "Data augmentation -- albumentations, torchvision transforms",
        "Video understanding -- optical flow, action recognition",
    ]:
        pdf.bullet(t)
    pdf.highlight_box(
        "Key Libraries",
        "torchvision, detectron2, OpenCV, albumentations, supervision, fiftyone"
    )

    # TRACK C
    pdf.sub_title("4.3  TRACK C -- ML Platform / Infra")
    pdf.body_text(
        "If you like DevOps, distributed systems, and making things run fast, this track "
        "makes you invaluable. You are the person who makes the data scientists' code actually "
        "work in production."
    )
    for t in [
        "Docker & Kubernetes -- containerise and orchestrate ML workloads",
        "Feature stores -- Feast, Tecton -- serve features consistently",
        "Model registries -- MLflow, BentoML -- version models like code",
        "CI/CD for ML -- DVC, CML, GitHub Actions for pipelines",
        "Distributed training -- Ray, DeepSpeed, FSDP -- train across multiple GPUs",
        "Monitoring -- Prometheus + Grafana, model drift detection",
        "Infrastructure as Code -- Terraform, Pulumi",
    ]:
        pdf.bullet(t)

    # ==================================================================
    #  5 - MONTHS 10-12: PRODUCTION & PORTFOLIO
    # ==================================================================
    pdf.add_page()
    pdf.section_title("5", "Months 10-12 -- Production & Portfolio")

    pdf.sub_title("5.1  Docker, CI/CD, Model Serving")
    pdf.body_text(
        "A model in a Jupyter notebook is a prototype. A model in a Docker container behind "
        "an API is a product. Learn how to bridge the gap:"
    )
    for s in [
        "Write a FastAPI app that loads your model and returns predictions via POST",
        "Write a Dockerfile that bundles your model + code + dependencies",
        "Add tests that run in CI (GitHub Actions)",
        "Deploy to a cloud VM or serverless (Railway, Modal, Hugging Face Spaces)",
        "Add a simple frontend (Gradio or Streamlit) so anyone can try it",
    ]:
        pdf.bullet(s)

    pdf.sub_title("5.2  Monitoring & Evaluation")
    pdf.body_text(
        "Models degrade over time (data drift, concept drift). You need to know when:"
    )
    for m in [
        "Log predictions and ground truth -- store them so you can compare",
        "Track accuracy / latency over time -- set up a dashboard",
        "Alerts -- if accuracy drops below 80%, notify someone",
        "Shadow / A/B testing -- compare your new model vs the old one on real traffic",
    ]:
        pdf.bullet(m)

    pdf.sub_title("5.3  Portfolio Projects That Stand Out")
    pdf.body_text(
        "Your portfolio is more important than your resume. Build projects that show depth, "
        "not just completion of a tutorial. Aim for 3 projects:"
    )

    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(*LIGHT_BG)
    pdf.set_x(pdf._lm)
    pdf.cell(pdf._full_w(), 7, "  Project 1: End-to-End RAG Chatbot", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "Ingest PDFs, embed them into a vector DB, answer questions with an LLM. "
        "Add evaluation (RAGAS scores), a Streamlit UI, deploy on Hugging Face Spaces. "
        "Show you understand the full pipeline from document to answer."
    )
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(*LIGHT_BG)
    pdf.set_x(pdf._lm)
    pdf.cell(pdf._full_w(), 7, "  Project 2: Deep-Dive Implementation", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "Implement something from scratch to prove you understand the internals: "
        "a small transformer, a GAN that generates handwritten digits, "
        "or a custom training loop with mixed precision. A blog post explaining your "
        "implementation doubles the impact."
    )
    pdf.set_font("Arial", "B", 10)
    pdf.set_fill_color(*LIGHT_BG)
    pdf.set_x(pdf._lm)
    pdf.cell(pdf._full_w(), 7, "  Project 3: Open Source Contribution", fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.body_text(
        "Fix a documentation bug, add a test, or implement a small feature in a library "
        "you use. This shows you can read other people's code and work in a team. "
        "Even a 5-line fix counts -- the goal is to experience the PR process."
    )

    # ==================================================================
    #  6 - RESOURCES
    # ==================================================================
    pdf.add_page()
    pdf.section_title("6", "Resources & Links")
    pdf.body_text(
        "A curated list of the best free (or cheap) resources. Do not try to consume "
        "all of them. Pick one per topic and finish it."
    )
    pdf.resources_block([
        ("Learn by Building",
         "Fast.ai Practical Deep Learning -- teaches top-down: you build a working model in "
         "the first lesson, then learn the theory. Best for motivation."),
        ("CS Theory (the fun way)",
         "Stanford CS229 (Andrew Ng) on YouTube. Old but gold. Also: Andrej Karpathy's "
         "Neural Networks: Zero to Hero playlist."),
        ("LLMs Specifically",
         "Andrej Karpathy 'Let's build GPT' -- builds a mini GPT from scratch in 2 hours. "
         "Hugging Face NLP course -- practical, hands-on."),
        ("Production ML",
         "Made With ML (madewithml.com) -- full-stack ML project. "
         "Full Stack Deep Learning course -- covers the entire lifecycle."),
        ("Stay Current",
         "The Gradient newsletter. Arxiv abstracts (curated). "
         "r/MachineLearning on Reddit (filter by [D] discussion). "
         "Follow Karpathy, Jay Alammar, Lilian Weng on Twitter / blogs."),
        ("Practice & Compete",
         "Kaggle -- datasets, competitions, notebooks. Do not spend too long on ranking; "
         "use it for structured practice."),
        ("Communities",
         "PyTorch Discord, Hugging Face Discord, local AI meetups. Find study buddies -- "
         "learning alone is harder."),
    ])

    # ==================================================================
    #  7 - WEEKLY ACTION PLAN
    # ==================================================================
    pdf.add_page()
    pdf.section_title("7", "Weekly Action Plan")
    pdf.body_text(
        "Consistency beats intensity. 10 hours per week for 52 weeks = 520 hours. "
        "That is enough to become employable. Here is a sample weekly schedule:"
    )
    pdf.ln(2)

    for day, time, desc in [
        ("Weekday (Mon-Fri)", "1 hour each evening",
         "Watch a lecture OR code for 45 min + write notes for 15 min. "
         "Small daily wins compound."),
        ("Saturday", "2-3 hours",
         "Deep work: build something. No passive watching. Start a mini-project "
         "and push to GitHub."),
        ("Sunday", "1 hour",
         "Review the week. Read 1 blog post. Plan next week. Rest."),
    ]:
        pdf.set_font("Arial", "B", 10)
        pdf.set_text_color(*BLUE)
        pdf.set_x(pdf._lm)
        pdf.cell(40, 6, day)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(*GRAY)
        pdf.cell(30, 6, time)
        pdf.set_x(pdf._lm)
        pdf.ln(6)
        pdf.set_text_color(*BLACK)
        pdf.set_x(pdf._lm)
        pdf.multi_cell(pdf._full_w(), 5.5, desc)
        pdf.ln(2)

    pdf.sub_title("Monthly Milestones Checklist")
    for m, desc in [
        ("Month 1",  "numpy + pandas basics done. Can load, filter, and plot a dataset."),
        ("Month 2",  "Wrote linear regression from scratch. Understands gradient descent."),
        ("Month 3",  "scikit-learn pipeline works on a real dataset. Knows train/test split."),
        ("Month 4",  "PyTorch basics: tensors, autograd, nn.Module. Trained a tiny network."),
        ("Month 5",  "Cat vs dog classifier works. Understands CNNs and transfer learning."),
        ("Month 6",  "FastAPI serving + experiment tracking set up. Can compare runs."),
        ("Month 7",  "Chosen a specialisation. Deep into it (LLMs / Vision / Infra)."),
        ("Month 8",  "Built a project in your specialisation (RAG chatbot, object detector)."),
        ("Month 9",  "Second project done. Starting to think about deployment."),
        ("Month 10", "Docker + CI/CD pipeline working. Model served behind an API."),
        ("Month 11", "All 3 portfolio projects solid. Blog posts written for 2 of them."),
        ("Month 12", "Applied to jobs / freelance. One mock interview per week."),
    ]:
        pdf.milestone_row(m, desc)

    # ==================================================================
    #  8 - THE SECRET SAUCE
    # ==================================================================
    pdf.add_page()
    pdf.section_title("8", "The Secret Sauce")
    pdf.body_text(
        "Everyone says 'learn AI' but most people fail because they:"
    )
    for f in [
        "Watch 100 hours of courses and never build anything --> tutorial hell.",
        "Try to learn ALL the math first --> burn out before writing a single line of ML code.",
        "Compare themselves to YouTube geniuses --> feel stupid and quit.",
    ]:
        pdf.bullet(f)
    pdf.ln(1)

    pdf.body_text(
        "Your cheat code: build one dumb thing every 2 weeks. A price predictor. "
        "A cat detector. A 'does this email look like spam?' filter. "
        "Each one teaches you more than a textbook chapter."
    )

    pdf.highlight_box(
        "Golden Rules",
        "1. Code > Watch -- always. When you are tired, it is okay to watch a lecture. "
        "But when you have energy, code.\n"
        "2. Ship early -- a bad project on GitHub is worth more than a perfect one in your head.\n"
        "3. Teach to learn -- write blog posts, make videos, explain to friends. "
        "Teaching reveals gaps in your understanding.\n"
        "4. AI is a tool, not magic -- know when to use it and when not to. "
        "A simple rule-based system often beats a complex model.\n"
        "5. You will feel stupid -- every single day. That is how learning feels. "
        "Keep going."
    )
    pdf.ln(6)

    # -- final motivational quote ---------------------------------------------
    pdf.set_font("Arial", "I", 14)
    pdf.set_text_color(*BLUE)
    pdf.set_x(pdf._lm)
    pdf.cell(pdf._full_w(), 10, '"The best time to start was yesterday.', align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(pdf._full_w(), 10, 'The second best time is now."', align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*GRAY)
    pdf.cell(pdf._full_w(), 6, "Good luck. You have got this!  ", align="C",
             new_x="LMARGIN", new_y="NEXT")

    # ==================================================================
    #  SAVE
    # ==================================================================
    out = r"r:\Test\ai-engineer-roadmap\AI_Engineer_in_1_Year_Roadmap.pdf"
    pdf.output(out)
    print(f"PDF saved to: {out}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == "__main__":
    build()
