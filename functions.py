def mix_colors(color1, color2, percent1):
    # mixes two colors based on given percentages

    r = int(color1[0] * percent1 + color2[0] * (1 - percent1))
    g = int(color1[1] * percent1 + color2[1] * (1 - percent1))
    b = int(color1[2] * percent1 + color2[2] * (1 - percent1))

    return (r, g, b)