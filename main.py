from src.loader import load_pdf


from src.loader import load_pdf


def main():
    print("Starting program...")

    file_path = "data/sample.pdf"
    print("Loading PDF from:", file_path)

    text = load_pdf(file_path)

    print("PDF loaded successfully.")
    print("Total characters extracted:", len(text))
    print("\nFirst 500 characters:\n")
    print(text[:500])


if __name__ == "__main__":
    main()