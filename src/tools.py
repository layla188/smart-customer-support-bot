import requests

from src.retrieval import retrieve_documents
from src.reranker import create_reranker, rerank_documents
ranker = create_reranker()


# ============================================================
# Tool 1: Search LumaCart Knowledge Base
# ============================================================

def search_knowledge_base(query: str) -> str:
    """
    Search the LumaCart knowledge base using vector retrieval
    followed by FlashRank reranking.

    Use this tool for questions about LumaCart products,
    shipping, returns, payments, support, and company policies.
    """

    try:

        # Step 1: Retrieve candidate documents from FAISS
        documents = retrieve_documents(
            query=query,
            top_k=10,
        )

        if not documents:
            return "No relevant information was found in the LumaCart knowledge base."

        # Step 2: Rerank retrieved documents
        reranked_documents = rerank_documents(
            query=query,
            documents=documents,
            ranker=ranker,
        )

        if not reranked_documents:
            return "No relevant information was found after reranking."

        results = []

        for i, document in enumerate(
            reranked_documents,
            start=1,
        ):

            page = document.metadata.get("page")

            if page is not None:
                page_number = page + 1
                source = f"Page {page_number}"
            else:
                source = "Unknown page"

            score = document.metadata.get(
                "rerank_score",
                "N/A",
            )

            results.append(
                f"[Source {i} - {source}]\n"
                f"{document.page_content}"
            )

        return "\n\n".join(results)

    except Exception as e:

        return f"Knowledge base search failed: {str(e)}"


# ============================================================
# Tool 2: Calculate Order Total
# ============================================================

def calculate_order_total(
    subtotal: float,
    discount_percent: float = 0,
    shipping_fee: float = 0,
) -> str:
    """
    Calculate the final LumaCart order total after applying
    a discount and adding shipping fees.
    """

    if subtotal < 0:
        return "Error: subtotal cannot be negative."

    if shipping_fee < 0:
        return "Error: shipping fee cannot be negative."

    if discount_percent < 0 or discount_percent > 100:
        return "Error: discount_percent must be between 0 and 100."

    discount_amount = subtotal * (discount_percent / 100)

    total_after_discount = subtotal - discount_amount

    final_total = total_after_discount + shipping_fee

    return (
        f"Subtotal: {subtotal:.2f} EGP\n"
        f"Discount: {discount_amount:.2f} EGP\n"
        f"Shipping: {shipping_fee:.2f} EGP\n"
        f"Final total: {final_total:.2f} EGP"
    )


# ============================================================
# Tool 3: Live Exchange Rate
# ============================================================

def get_exchange_rate(
    from_currency: str,
    to_currency: str,
    amount: float = 1.0,
) -> str:
    """
    Get the latest available exchange rate and convert
    an amount from one currency to another using
    Frankfurter's live exchange-rate API.
    """

    if amount < 0:
        return "Error: amount cannot be negative."

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if len(from_currency) != 3 or len(to_currency) != 3:
        return (
            "Error: currencies must use valid 3-letter "
            "currency codes such as USD, EUR, or EGP."
        )

    if from_currency == to_currency:
        return (
            f"{amount:.2f} {from_currency} = "
            f"{amount:.2f} {to_currency}"
        )

    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{from_currency.lower()}/"
        f"{to_currency.lower()}"
    )

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "LumaAssist/1.0"
            },
        )

        response.raise_for_status()

        data = response.json()

        rate = data.get("rate")

        if rate is None:
            return (
                f"I couldn't retrieve the exchange rate "
                f"for {from_currency} to {to_currency}."
            )

        rate = float(rate)

        converted_amount = amount * rate

        date = data.get(
            "date",
            "latest available date",
        )

        return (
            f"Exchange rate date: {date}\n"
            f"1 {from_currency} = "
            f"{rate:.4f} {to_currency}\n"
            f"{amount:.2f} {from_currency} = "
            f"{converted_amount:.2f} {to_currency}"
        )

    except requests.exceptions.Timeout:

        return (
            "The exchange-rate service took too long "
            "to respond. Please try again."
        )

    except requests.exceptions.ConnectionError:

        return (
            "The live exchange-rate service is currently "
            "unreachable. Please try again shortly."
        )

    except requests.exceptions.HTTPError as error:

        return (
            "The exchange-rate service returned an error: "
            f"{error}"
        )

    except requests.RequestException as error:

        return (
            "The live exchange-rate service is temporarily "
            f"unavailable: {error}"
        )

    except (TypeError, ValueError, KeyError):

        return (
            "The exchange-rate service returned an "
            "unexpected response."
        )


TOOLS = [
    search_knowledge_base,
    calculate_order_total,
    get_exchange_rate,
]

if __name__ == "__main__":

    print("\n--- Knowledge Base Tool ---")

    print(
        search_knowledge_base(
            "What payment methods are available?"
        )
    )

    print("\n--- Order Total Tool ---")

    print(
        calculate_order_total(
            subtotal=800,
            discount_percent=10,
            shipping_fee=50,
        )
    )

    print("\n--- Live Exchange Rate Tool ---")

    print(
        get_exchange_rate(
            from_currency="USD",
            to_currency="EGP",
            amount=10,
        )
    )