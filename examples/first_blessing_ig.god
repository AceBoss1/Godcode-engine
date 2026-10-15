# tongue: ig
# Ndewo. The first blessing spoken in Igbo.
# Run it: godcode run examples/first_blessing_ig.god
# Dotted vowels are optional: GOSIPỤTA and GOSIPUTA both speak.
MALITE OKIKE
KWUPỤTA aha DỊKA "enyi m"
GOSIPỤTA("Ndewo, {aha}.")

KWUPỤTA ubochi DỊKA ["Eke", "Orie", "Afọ", "Nkwọ"]
GOSIPỤTA("Ụbọchị ahịa anọ: {ubochi}")

Ọ BỤRỤ LEN(ubochi) BỤ 0 MGBE AHỤ
    GOSIPỤTA("Enweghị ụbọchị")
ELSE
    GOSIPỤTA("Ụbọchị ahịa dị {LEN(ubochi)}")
NJEDEBE MA

NWAA
    KWUPỤTA oke DỊKA 10 / 0
JIDE
    GOSIPỤTA("E jidere njehie, mana ọrụ ka na-aga n'ihu")
NJEDEBE NWAA

GOSIPỤTA("Daalụ.")
NJEDEBE OKIKE
