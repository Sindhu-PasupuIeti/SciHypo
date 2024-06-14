# Load model directly
import openai
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("lmsys/vicuna-13b-v1.3")
model = AutoModelForCausalLM.from_pretrained("lmsys/vicuna-13b-v1.3")

# Function for generating summary
openai.api_key = 'OPEN API KEY'

# Function for generating hypotheses
def generate_hypotheses(document_text):
    # Define the prompt
    prompt = f"Given the following research document:\n{document_text}\n\nBased on the above document, generate new avenues for further exploration."

    # Set the parameters for the completion
    response = openai.completions.create(
        model=model,  # Model to use
        prompt= prompt,
        max_tokens= 150,  # Adjust the length of the generated text
        temperature=0.7,  # Controls the randomness of the generated text
        n=2,  # Number of completions to generate
        stop=None,  # Stop condition for the completion
        stream=False  # Set stream to False to receive all completions at once
    )

    # Extract and return the generated hypotheses
    hypotheses = [completion['choices'][0]['text'].strip() for completion in response['choices']]
    return hypotheses

document_text = """In the course of this innovative study, we delve into the dynamic landscape of Deep 
Convolutional Generative Adversarial Networks, specifically exploring their application in 
the domain of anime face synthesis. The main focus of our examination revolves around 
elucidating the intricate theory behind GANs and furnishing a comprehensive guide on 
constructing a DCGAN model tailored for the synthesis of anime faces. We meticulously 
detail the steps involved in training and developing the generator and discriminator models, 
customizing them to efficiently cater to the unique features of anime characters. Our 
evaluation, which resulted in respective losses of 1.7594 for the generator and 0.4533 for the 
discriminator, underscores the efficacy and adaptability of our approach in the realm of anime 
face synthesis."""
hypotheses = generate_hypotheses(document_text)
for i, hypothesis in enumerate(hypotheses, start=1):
    print(f"Hypothesis {i}: {hypothesis}")