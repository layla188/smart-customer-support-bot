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
    an amount from one currency to another.
    """

    if amount < 0:
        return "Error: amount cannot be negative."

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    if len(from_currency) != 3 or len(to_currency) != 3:
        return (
            "Error: currencies must use 3-letter codes "
            "such as USD or EUR."
        )

    if from_currency == to_currency:
        return (
            f"{amount:.2f} {from_currency} = "
            f"{amount:.2f} {to_currency}"
        )

    url = "https://api.frankfurter.app/latest"

    try:

        response = requests.get(
            url,
            params={
                "from": from_currency,
                "to": to_currency,
            },
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        rates = data.get("rates", {})

        if to_currency not in rates:
            return (
                f"Exchange rate for {from_currency} "
                f"to {to_currency} is not available."
            )

        rate = rates[to_currency]

        converted_amount = amount * rate

        return (
            f"Latest available rate: "
            f"1 {from_currency} = {rate:.4f} {to_currency}\n"
            f"{amount:.2f} {from_currency} = "
            f"{converted_amount:.2f} {to_currency}"
        )

    except requests.RequestException as e:

        return (
            f"Live exchange-rate service is unavailable: "
            f"{str(e)}"
        )

    except (KeyError, TypeError, ValueError) as e:

        return f"Invalid exchange-rate response: {str(e)}"


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
            to_currency="EUR",
            amount=100,
        )
    )