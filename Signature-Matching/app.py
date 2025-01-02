import argparse
from signature import match

# Match Threshold
THRESHOLD = 85

def check_similarity(path1, path2):
    """
    Compare two signatures and print the similarity result.
    """
    try:
        result = match(path1=path1, path2=path2, show_image=False)  
        if result <= THRESHOLD:
            print(f"Failure: Signatures do not match. Similarity: {result} %")
        else:
            print(f"Success: Signatures match. Similarity: {result} %")
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Compare two signature images for similarity.")
    parser.add_argument(
        "--path1", type=str, help="Path to the first signature image", required=True
    )
    parser.add_argument(
        "--path2", type=str, help="Path to the second signature image", required=True
    )

    args = parser.parse_args()

    # Directly use the provided paths for comparison
    path1 = args.path1.strip()
    path2 = args.path2.strip()

    check_similarity(path1, path2)

if __name__ == "__main__":
    main()
