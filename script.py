import gradio as gr
import modules.shared as shared
#import numpy as np

params = {
        "display_name": "Token Loupe",
        "is_tab": False,
        'enable_cap': True,
}
pastel_colors = [
    "rgba(107,64,216,.3)",
    "rgba(104,222,122,.4)",
    "rgba(244,172,54,.4)",
    "rgba(239,65,70,.4)",
    "rgba(39,181,234,.4)",
]

last_tokens = []

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Define ANSI escape codes for text and background colors
PASTEL_TEXT = "\033[97m"  # White text
BLACK_TEXT = "\033[30m"
PASTEL_BG = "\033[48;5;"  # Start of background color code
RESET = "\033[0m"
# Function to escape special characters
def escape_special_chars(decoded_token):
    # Escape \n, \r, and \t
    decoded_token = decoded_token.replace("\n", "\\n")
    decoded_token = decoded_token.replace("\r", "\\r")
    decoded_token = decoded_token.replace("\t", "\\t")
    return decoded_token

def logits_processor_modifier(processor_list, input_ids):
    """
    Adds logits processors to the list, allowing you to access and modify
    the next token probabilities.
    Only used by loaders that use the transformers library for sampling.
    """
    global last_tokens
    last_tokens = input_ids.tolist()[0]
    #decoded_text = shared.tokenizer.decode(last_tokens)
    

    if params['enable_cap']:
            # Initialize an empty string to accumulate the output
        output_string = ""

        # Iterate through tokens and add formatted strings to the output
        for token in last_tokens:

            if token == 0:
                decoded_token = "<unk>"
            elif token == 1:
                decoded_token = "<s>"
            elif token == 2:
                decoded_token = "</s>"
            else:
                decoded_token = shared.tokenizer.decode([token])
                decoded_token = escape_special_chars(decoded_token)

            
            if token % 3 == 0:
                color = RED
            elif token % 3 == 1:
                color = GREEN
            else:
                color = YELLOW


            #ascii_values = []

            # Iterate through each character in decoded_token
            #for char in decoded_token:
                # Get the ASCII value of the character and append it to the list
            #    ascii_values.append(ord(char))

            # Convert the list of ASCII values to a string
            #ascii_values_str = ', '.join(map(str, ascii_values))    
            
            background_color = PASTEL_BG + str(200 + (token % 16)) + "m"

            # Add the formatted string to the output
            output_string += f"{background_color}{BLACK_TEXT} {decoded_token} {RESET}[{token}] " #[{token}]

    # Print the entire output in one line
    print(output_string)


    return processor_list

def display_tokens_tok():
    global last_tokens

    if shared.tokenizer is None:
        return "Tokenizer is not available. Please Load some Model first."
    html_tokens = ""
    encoded_tokens  = last_tokens
    decoded_tokens = []
    #print(encoded_tokens)
    for token in encoded_tokens:
        shared.tokenizer.decode
        chars = shared.tokenizer.decode([token])
        if token == 0:
            decoded_tokens.append("&lt;unk&gt;")
        elif token == 1:
            decoded_tokens.append("&lt;s&gt;")
        elif token == 2:
            decoded_tokens.append("&lt;/s&gt;")
        elif 3 <= token <= 258:
            vocab_by_id = f"&lt;0x{hex(token)[2:].upper()}&gt;"
            decoded_tokens.append(vocab_by_id)
        else:
            decoded_tokens.append(chars)

    for index, token in enumerate(decoded_tokens):
        #avoid jumpy artefacts
        if token=='':
            token = ' '
        html_tokens += f'<span style="background-color: {pastel_colors[index % len(pastel_colors)]}; ' \
                    f'padding: 0 4px; border-radius: 3px; margin-right: 0px; margin-bottom: 4px; ' \
                    f'display: inline-block; height: 1.5em;"><pre>{str(token).replace(" ", "&nbsp;")}</pre></span>'
        

    token_count = len(encoded_tokens)

    # Join the decimal values of encoded_tokens with commas
    token_values_str = ', '.join(map(str, encoded_tokens))

    # Append the token values to the HTML
    html_tokens += f'<div style="font-size: 14px; margin-top: 10px;">Token Values: {token_values_str}</div>'

    html_tokens += f'<div style="font-size: 18px; margin-top: 10px;">Token Count: {token_count}</div>'
         
    return html_tokens

def display_tokens(text):
    html_tokens = ""

    if shared.tokenizer is None:
        return "Tokenizer is not available. Please Load some Model first."
    
    encoded_tokens  = shared.tokenizer.encode(str(text))

    decoded_tokens = []
    #print(encoded_tokens)
    for token in encoded_tokens:
        shared.tokenizer.decode
        chars = shared.tokenizer.decode([token])
        if token == 0:
            decoded_tokens.append("&lt;unk&gt;")
        elif token == 1:
            decoded_tokens.append("&lt;s&gt;")
        elif token == 2:
            decoded_tokens.append("&lt;/s&gt;")
        elif 3 <= token <= 258:
            vocab_by_id = f"&lt;0x{hex(token)[2:].upper()}&gt;"
            decoded_tokens.append(vocab_by_id)
        else:
            decoded_tokens.append(chars)

    for index, token in enumerate(decoded_tokens):
        #avoid jumpy artefacts
        if token=='':
            token = ' '
        html_tokens += f'<span style="background-color: {pastel_colors[index % len(pastel_colors)]}; ' \
                    f'padding: 0 4px; border-radius: 3px; margin-right: 0px; margin-bottom: 4px; ' \
                    f'display: inline-block; height: 1.5em;"><pre>{str(token).replace(" ", "&nbsp;")}</pre></span>'
        

    token_count = len(encoded_tokens)

    # Join the decimal values of encoded_tokens with commas
    token_values_str = ', '.join(map(str, encoded_tokens))

    # Append the token values to the HTML
    html_tokens += f'<div style="font-size: 14px; margin-top: 10px;">Token Values: {token_values_str}</div>'

    html_tokens += f'<div style="font-size: 18px; margin-top: 10px;">Token Count: {token_count}</div>'
         
    return html_tokens

def ui():
    enable_cap = gr.Checkbox(value=params['enable_cap'], label='Live Print Tokens in Terminal')
    with gr.Accordion("Tokens", open=True):
        tokenhtml = gr.HTML(visible=True)
        tokenize = gr.Button(value='Display last captured tokens')
        inp_text = gr.Textbox(value = '', lines=3,label='Custom Text')
        tokenhtml2 = gr.HTML(visible=True)
        tokenize_inp = gr.Button(value='Tokenize Custom Text')

    tokenize.click(display_tokens_tok,None,tokenhtml)
    tokenize_inp.click(display_tokens,inp_text,tokenhtml2)
    enable_cap.change(lambda x: params.update({"enable_cap": x}), enable_cap, None)