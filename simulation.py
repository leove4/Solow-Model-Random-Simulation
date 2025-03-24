import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# définition d'une fonction pour la simulation en suivant le modèle de Solow
def simulation():
    k0       = slider_k.val
    a0       = slider_a.val
    l0       = slider_l.val
    seuil    = slider_seuil.val
    seuilmin = slider_seuilmin.val
    s        = slider_s.val
    delta    = slider_delta.val

    n_trans_max = slider_n_trans_max.val

    g_min  = slider_g_min.val
    g_max  = slider_g_max.val

    n_post_min  = slider_n_post_min.val
    n_post_max  = slider_n_post_max.val

    event_t   = int(slider_event_t.val)
    event_val = slider_event_val.val

    k = k0
    a = a0
    l = l0
    Y = (k**0.5) * ((a * l)**0.5)
    y = Y / (a * l)
    t = 0

    # listes pour enregistrer l'évolution des valeurs
    T   = []
    pib = []
    PIB = []
    LN  = []
    a_list = []
    
    T.append(t)
    PIB.append(Y)
    pib.append(y)
    LN.append(l)
    a_list.append(a)

    transition = False

    while t < 1000:
        if not transition:
            if l < seuil:
                # pas de transition démographique
                g = np.random.uniform(g_min, g_max)
                a = a + g * a
                
                #évenement
                if t == event_t:
                    l = l * (1 + event_val)

                
                n = np.random.uniform(0, n_trans_max)
                l = l + n * l
                k = k + s * Y - delta * k
                Y = (k**0.5) * ((a * l)**0.5)
                y = Y / (a * l)
                t += 1
                
                
                T.append(t)
                PIB.append(Y)
                pib.append(y)
                LN.append(l)
                a_list.append(a)
            if l >= seuil:
                transition = True

        if transition:
            # transition démograpgique
            g = np.random.uniform(g_min, g_max)
            a = a + g * a
               
            #evenement
            if t == event_t:
                l = l * (1 + event_val)

            if l > seuilmin:
                n = np.random.uniform(n_post_min, n_post_max)
            else:
                transition = False

            l = l + n * l
            k = k + s * Y - delta * k
            Y = (k**0.5) * ((a * l)**0.5)
            y = Y / (a * l)
            t += 1
            
         
            T.append(t)
            PIB.append(Y)
            pib.append(y)
            LN.append(l)
            a_list.append(a)

    return T, pib, PIB, LN, a_list

#Fonction pour avoir un graphique dynamique

def update(val):
    T, pib_vals, PIB_vals, LN_vals, a_vals = simulation()
    line_pib.set_data(T, pib_vals)
    line_pib_tot.set_data(T, PIB_vals)
    line_ln.set_data(T, LN_vals)
    line_a.set_data(T, a_vals)
    line_gdp.set_data(T, pib_vals)  
    
    evt_t = slider_event_t.val
    line_event.set_xdata([evt_t, evt_t])
    
    # ajustement de l'échelle du nouveau graphique
    ax.relim()
    ax.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    ax_gdp.relim()
    ax_gdp.autoscale_view()
    fig.canvas.draw_idle()

# fonction pour créer un slider
def create_slider(ax_obj, titre, description, min_val, max_val, init):
    sld = Slider(ax_obj, "", min_val, max_val, valinit=init)
    ax_obj.set_title(f"{titre}\n{description}", fontsize=8, pad=4)
    return sld

# création du cadre de la figure
fig = plt.figure(figsize=(14, 10))

# axe principal
ax = fig.add_axes([0.1, 0.6, 0.8, 0.35])
# deuxième axe pour graph a
ax2 = ax.twinx()

#légende pour les sliders
fig.text(0.25, 0.53, "paramètres de départ", ha="center", va="bottom", fontsize=10)
fig.text(0.75, 0.53, "probabilités et événement", ha="center", va="bottom", fontsize=10)

# position des sliders 
left_slider_x = 0.1
left_slider_width = 0.35
start_y_left = 0.45
height = 0.03
gap = 0.02

ax_slider_k = fig.add_axes([left_slider_x, start_y_left, left_slider_width, height])
slider_k = create_slider(ax_slider_k, "k", "capital initial de l'économie", 0.1, 10, 1)

ax_slider_a = fig.add_axes([left_slider_x, start_y_left - (height+gap)*1, left_slider_width, height])
slider_a = create_slider(ax_slider_a, "a", "niveau de productivité (technologie)", 0.1, 10, 1)

ax_slider_l = fig.add_axes([left_slider_x, start_y_left - (height+gap)*2, left_slider_width, height])
slider_l = create_slider(ax_slider_l, "l", "population initiale (travail)", 0.1, 10, 1)

ax_slider_seuil = fig.add_axes([left_slider_x, start_y_left - (height+gap)*3, left_slider_width, height])
slider_seuil = create_slider(ax_slider_seuil, "seuil", "population déclenchant transition", 1, 20, 5)

ax_slider_seuilmin = fig.add_axes([left_slider_x, start_y_left - (height+gap)*4, left_slider_width, height])
slider_seuilmin = create_slider(ax_slider_seuilmin, "seuil min", "population minimale stable", 0.1, 5, 1)

ax_slider_s = fig.add_axes([left_slider_x, start_y_left - (height+gap)*5, left_slider_width, height])
slider_s = create_slider(ax_slider_s, "s", "taux d'épargne réinvesti", 0, 1, 0.2)

ax_slider_delta = fig.add_axes([left_slider_x, start_y_left - (height+gap)*6, left_slider_width, height])
slider_delta = create_slider(ax_slider_delta, "delta", "taux de dépréciation du capital", 0, 1, 0.05)

# sliders à droite 
right_slider_x = 0.55
right_slider_width = 0.35
start_y_right = 0.45

ax_slider_g_min = fig.add_axes([right_slider_x, start_y_right, right_slider_width, height])
slider_g_min = create_slider(ax_slider_g_min, "g min", "croissance tech minimum", -0.1, 0, -0.02)

ax_slider_g_max = fig.add_axes([right_slider_x, start_y_right - (height+gap)*1, right_slider_width, height])
slider_g_max = create_slider(ax_slider_g_max, "g max", "croissance tech maximum", 0, 0.1, 0.02)

ax_slider_n_trans_max = fig.add_axes([right_slider_x, start_y_right - (height+gap)*2, right_slider_width, height])
slider_n_trans_max = create_slider(ax_slider_n_trans_max, "n trans max", "croissance max pop. transition", 0, 0.1, 0.02)

ax_slider_n_post_min = fig.add_axes([right_slider_x, start_y_right - (height+gap)*3, right_slider_width, height])
slider_n_post_min = create_slider(ax_slider_n_post_min, "n post min", "var. min pop. post-trans", -0.1, 0, -0.04)

ax_slider_n_post_max = fig.add_axes([right_slider_x, start_y_right - (height+gap)*4, right_slider_width, height])
slider_n_post_max = create_slider(ax_slider_n_post_max, "n post max", "var. max pop. post-trans", 0, 0.1, 0.02)

ax_slider_event_t = fig.add_axes([right_slider_x, start_y_right - (height+gap)*5, right_slider_width, height])
slider_event_t = create_slider(ax_slider_event_t, "event t", "temps événement (afflux/chute)", 0, 1000, 500)

ax_slider_event_val = fig.add_axes([right_slider_x, start_y_right - (height+gap)*6, right_slider_width, height])
slider_event_val = create_slider(ax_slider_event_val, "event val", "valeur relative de l'événement (+/-)", -0.5, 0.5, 0.1)

# Lance la simulation initiale
T, pib_vals, PIB_vals, LN_vals, a_vals = simulation()

# légende et labels
line_pib,     = ax.plot(T, pib_vals,     label='pib per capita')
line_pib_tot, = ax.plot(T, PIB_vals,     label='pib total')
line_ln,      = ax.plot(T, LN_vals,      label='population')
line_a,       = ax2.plot(T, a_vals, color='red', label='niveau de a')

# Ligne pour montrer le moment de l'événement
event_init_x = slider_event_t.val
line_event = ax.axvline(event_init_x, color='r', linestyle='--', label="événement")

ax.set_xlabel("temps")
ax.set_ylabel("pib / population")
ax2.set_ylabel("niveau de a", color='red')
ax.legend(loc='upper left')
ax2.legend(loc='upper right')
ax.grid(True)

# partie pour montrer seulement le gdp par capita
ax_gdp = fig.add_axes(ax.get_position().bounds)
line_gdp, = ax_gdp.plot(T, pib_vals, label='Pib par tête', color='green')
ax_gdp.set_xlabel("temps")
ax_gdp.set_ylabel("Pib par tête")
ax_gdp.legend()
ax_gdp.grid(True)
ax_gdp.set_visible(False)  # caché de base

# boutons pour switch
ax_radio = fig.add_axes([0.82, 0.035, 0.13, 0.12])
radio = RadioButtons(ax_radio, ('Afficher Tout', 'PIB par tête'))

def switch_view(label):
    if label == 'Afficher Tout':
        ax.set_visible(True)
        ax2.set_visible(True)
        ax_gdp.set_visible(False)
    elif label == 'PIB par tête':
        ax.set_visible(False)
        ax2.set_visible(False)
        ax_gdp.set_visible(True)
    fig.canvas.draw_idle()

radio.on_clicked(switch_view)

# Permet d'actualiser en direct les valeurs des sliders
slider_k.on_changed(update)
slider_a.on_changed(update)
slider_l.on_changed(update)
slider_seuil.on_changed(update)
slider_seuilmin.on_changed(update)
slider_s.on_changed(update)
slider_delta.on_changed(update)
slider_g_min.on_changed(update)
slider_g_max.on_changed(update)
slider_n_trans_max.on_changed(update)
slider_n_post_min.on_changed(update)
slider_n_post_max.on_changed(update)
slider_event_t.on_changed(update)
slider_event_val.on_changed(update)

plt.show()
