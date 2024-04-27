# filename = 'main.py'

#
# Imports                                          ###########################
#

from re import template
import plotly_express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from collections import Counter
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from os import listdir
from os.path import isfile, join
import base64

#
# Data                                              ###########################
#

#lecture du fichier JSON
pokedex = pd.read_json('data/pokedex.json')


###################           Les variables              ######################   


#################### Data Carte géographique : Les Régions  ###################


#liste des noms pokemons en français
french_name = [pokedex['name'][i]['french'] for i in range(pokedex['name'].size)]
#liste de la somme des stats des pokemons
stats_scale = [pokedex['base'][i]['HP']+pokedex['base'][i]['Attack']+pokedex['base'][i]['Defense']+pokedex['base'][i]['Sp. Attack']+pokedex['base'][i]['Sp. Defense']+pokedex['base'][i]['Speed'] for i in range(pokedex['id'].size)]
#lecture du fichier csv
pokemon_location = pd.read_csv("data/pkm_location_by_region.csv")
map_value = "Région"


#################### Data Carte géographique : Les Régions  ###################


#################### Data Histogramme : Les Types ###################

pokemon_types = pd.read_json('data/types.json')

histo_value = "Type 1&2"

histo_dropdown_options = [{'label': pokemon_types["french"].unique()[i], 'value': pokemon_types["french"].unique()[i]} for i in range(pokemon_types["french"].size) ]

#Liste du premier et deuxième type de tous les Pokémons
first_type = [pokedex['type'][i][0] for i in range(pokedex['id'].size)]
second_type = [pokedex['type'][i][1] if len(pokedex['type'][i]) > 1 else 'null' for i in range(pokedex['id'].size)]

#Compteur de premier type suivi du nombre de deuxième type 
type_counter = list(Counter(first_type).items()) #only contain list of first type count for now
type1_count = list([type_counter[i][1] for i in range(len(type_counter))])
type1_list = list([type_counter[i][0] for i in range(len(type_counter))])

type2_counter = list(Counter(second_type).items())
type2_count = list([type2_counter[i][1] for i in range(len(type2_counter))  if type2_counter[i][0]!='null' ])
type2_list = list([type2_counter[i][0] for i in range(len(type2_counter))  if type2_counter[i][0]!='null' ])

#type1list & type1count est la concaténation de de type1 et type2
[type1_list.append(i) for i in type2_list]
[type1_count.append(i) for i in type2_count]

#Catégoriser les types de pokemons en Type 1 et Type 2
type1 = ['Type 1' for i in range(len(type2_count))]
type2 = ['Type 2' for i in range(len(type2_count))]

[type1.append(i) for i in type2]

# Résumé : 
# type1_list => liste n types fois 2 
# type1 => liste de n 'Type 1' + n 'Type 2'
# type1_count => liste du nombre de pokemon avec le même premier type et deuxième type 

types_df = pd.DataFrame({
  "Type": type1_list ,
  "Types": type1,
  "Nombres": type1_count,
})


#################### Data Histogramme : Les Types ###################


####################        Les Fonctions           ######################


#################### Carte géographique : Les Régions  ###################


def map_graph(input_value):
    """
    Retourne le graphique des régions Pokémon.

    Args:
        void

    Returns:
        region_graph() : px.scatter_mapbox(..)
    """
    region_graph = px.scatter_mapbox(
        pokemon_location, 
        labels=dict([('id', 'ID'),('region','Region'),('size','Stats_tot'),('color','Type')]), 
        hover_name=french_name, 
        hover_data=["id","region"],
        lat="latitude", 
        lon="longitude", 
        color=input_value, 
        zoom=1, 
        width=750, 
        height = 500,
        size_max=15,
        size = stats_scale ,
    )
    region_graph.update_layout(mapbox_style="stamen-terrain",paper_bgcolor = '#F5F5F5',
        template = 'plotly_white')
    region_graph.update_layout(margin={"r":20,"t":20,"l":20,"b":20})
    return region_graph
    

#################### Carte géographique : Les Régions  ###################

#################### Histogramme : Les Types ###################

def types_histo(x_axis,legend):
    """
    Retourne l'histogramme des types.

    Args:
        void

    Returns:
        types_histo() : px.bar(..)
    """
    types_histo = px.bar(types_df, x=x_axis, y="Nombres", color=legend, barmode="group",height=500,width = 750,text = "Nombres")
    types_histo.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    types_histo.update_layout(
        yaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=False,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=False,
        ),
        paper_bgcolor = '#F5F5F5',
        template = 'plotly_white'
    )
    return types_histo


#################### Histogramme : Les Types ###################

###################### Pokédex : Comparez les statistiques des Pokémons entre eux #######################

#
#Display Image                                      ##################
#
id_left = '001'
id_right = '004'
region_left = 'Kanto'
region_right = 'Kanto'
list_pkm_png_name = [f for f in listdir('data/images') if isfile(join('data/images', f))]
dd1_pokemon_list = [{'label': french_name[i], 'value': pokedex['id'][i]} for i in range(pokedex['id'].size - 1 ) ]

def display_img(png_index):
    """
    Retourne l'image grande taille.

    Args:
        png_index

    Returns:
        display_img(png_index) : 'data:image/png;base64,{}'.format(encoded_image.decode())
    """
    image_filename = f'data/images/{list_pkm_png_name[png_index]}' 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

sprites_pkm_png_name = [f for f in listdir('data/sprites') if isfile(join('data/sprites', f))]
def display_sprite(png_index):
    """
    Retourne le sprite du Pokémon.

    Args:
        png_index

    Returns:
        display_sprite(png_index) : 'data:image/png;base64,{}'.format(encoded_image.decode())
    """
    image_filename = f'data/sprites/{sprites_pkm_png_name[png_index]}' 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

types_pkm_png_name = [f for f in listdir('data/types_images') if isfile(join('data/types_images', f))]



def display_type(type_index):
    """
    Retourne l'image du type.

    Args:
        type_index

    Returns:
        display_type(type_index) : 'data:image/png;base64,{}'.format(encoded_image.decode())
    """
    
    image_filename = f'data/types_images/{type_index}' 
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

english_type =np.sort(pokemon_types["english"].unique())

def select_type1(input_value):
    """
    Retourne l'image en fonction des données en anglais

    Args:
        input_value

    Returns:
        select_type1(input_value) : 'data:image/png;base64,{}'.format(encoded_image.decode())
    """
    src = [display_type(types_pkm_png_name[i]) for i in range(18) if first_type[input_value-1] == english_type[i]]

    return ''.join(src)

def select_type2(input_value):
    """
    Retourne l'image en fonction des données en anglais

    Args:
        input_value

    Returns:
        select_type2(input_value) : 'data:image/png;base64,{}'.format(encoded_image.decode())
    """
    src = [display_type(types_pkm_png_name[i]) for i in range(18) if second_type[input_value-1] == english_type[i]]

    return ''.join(src)
#
#Display Image                                          ##################
#


#
#Polar Chart Stats                                      ##################
#

stats_name = ['PV','Attaque','Défense','Atq. Spé.','Def. Spé.','Vitesse']

stats_name += [stats_name.pop(5)] + [stats_name.pop(4)] + [stats_name.pop(3)]

#changement d'ordre : ['PV', 'Attaque', 'Défense', 'Vitesse', 'Def. Spé.', 'Atq. Spé.']

def stats_graph(id_pkm1, id_pkm2):
    """
    Retourne le polar chart affichant les stats des 2 Pokémons

    Args:
        id_pkm1, id_pkm2

    Returns:
        stats_graph(id_pkm1, id_pkm2) : stats_fig1
    """
    first_pkm_stats = [k for k in pokedex['base'][id_pkm1].values()]
    first_pkm_stats += [first_pkm_stats.pop(5)] + [first_pkm_stats.pop(4)] + [first_pkm_stats.pop(3)]
    second_pkm_stats = [k for k in pokedex['base'][id_pkm2].values()]
    second_pkm_stats += [second_pkm_stats.pop(5)] + [second_pkm_stats.pop(4)] + [second_pkm_stats.pop(3)]

    stats_fig1 = px.line_polar(
        {'value':first_pkm_stats, 'stat':stats_name}, 
        r="value",
        theta="stat", 
        start_angle=90,
        line_close=True,
    )

    stats_fig2 = px.line_polar(
        {'value':second_pkm_stats, 'stat':stats_name}, 
        r="value", 
        color_discrete_sequence=["salmon"]*5,
        theta="stat",
        start_angle=90, 
        line_close=True,
        
        
    )

    
    stats_fig1.add_trace(stats_fig2.data[0])
    
    stats_fig1.update_traces(fill='toself')

    stats_fig1.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0,280]
            )
        ),
        showlegend=True,
        height = 450,
        width = 450,
        template = 'plotly_white',
        paper_bgcolor = '#F5F5F5'

    )
    return stats_fig1

#
#Polar Chart Stats                                      ##################                                      
#



#
#Bar Stats                                              ##################
#

bar_stats_name = ['PV','Attaque','Défense','Atq. Spé.','Def. Spé.','Vitesse']

bar_stats_name.reverse()


def stats_bar(id_pkm):
    """
    Retourne le bar chart du Pokémon

    Args:
        id_pkm

    Returns:
        stats_bar(id_pkm) : stats_bar
    """
    bar_pkm_stats = [k for k in pokedex['base'][id_pkm].values()]
    bar_pkm_stats.reverse()
    bar_color = ['SeaGreen' if bar_pkm_stats[i]>=100 else 'orange' if bar_pkm_stats[i]>=80 else 'Crimson' for i in range(6)]
    stats_bar = go.Figure(go.Bar(
                x=bar_pkm_stats,
                y=bar_stats_name,
                marker_color = bar_color,
                orientation='h',
                text = bar_pkm_stats,
                textposition = 'outside'
                ))

    stats_bar.update_layout(
        yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=False,
        ),
        plot_bgcolor='#F5F5F5',
        height = 200,
        width = 525,
        margin=dict(l=0, r=0, t=20, b=20),
        paper_bgcolor="#F5F5F5"
    )


    return stats_bar

#
#Bar stats                                      ##################
#

###################### Pokédex : Comparez les statistiques des Pokémons entre eux #######################

#
# Main                                          ##################
#

if __name__ == '__main__':

    app = dash.Dash(__name__) # (3)On crée une instance de la classe Dash
    app.title = 'PokéData'
    #
    #Dashboard Layout                           ##################
    #

    app.layout = html.Div([
        html.H1(
                    children=f'PokéData',
                    style={'textAlign': 'center','font-family' : 'sans-serif' , 'background-color' : '#0A285F', 'color' : '#FFCC00' , 'margin' :'5px 0px', 'padding' : '10px 0px' }
                ), 
        #
        #Carte géographique                     ##################
        #
        html.Div(
            children=[
                html.H1(
                    children=f'La Carte',
                    style={'textAlign': 'center','font-family' : 'sans-serif' , 'background-color' : '#0075BE', 'color' : 'white' , 'margin' :'5px 0px', 'padding' : '10px 0px' }
                ), 
                dcc.Dropdown(
                    id = 'map_dropdown',
                    options=[
                        {'label': 'Carte Régions', 'value': 'region'},
                        {'label': 'Carte Types 1', 'value': 'type1'},
                        {'label': 'Carte Types 2', 'value': 'type2'}
                    ],
                    value = 'region',
                    clearable=False,
                    style = {"font-weight":"bold",'border-radius' : '10px','font-family' : 'sans-serif','background-color' : '#5EBDFC'}
                ),
                
                html.Div(children=[
                    dcc.Graph(
                        id ="map_graph",
                        figure = map_graph('region')
                    )
                ],
                style={'textAlign': 'center', 'width' : '750'}
                ),
                html.H3(
                    id = 'map_title',
                    children=f'Carte des {map_value} ',
                    style={'textAlign': 'center', 'font-family' : 'sans-serif' }
                ),
                
            ],
            style={'display':'inline-block', 'width' : '750','text-align' : 'center'}
        ),
        #
        #Carte géographique                     ##################
        #

        #
        #Histo                                  ##################
        #
        html.Div(
            children=[
                html.H1(
                    children=f'Les Types',
                    style={'textAlign': 'center','font-family' : 'sans-serif', 'background-color' : '#FFCC00', 'color' : 'white' , 'margin' :'5px 0px', 'padding' : '10px 0px'  }
                ),
                dcc.Dropdown(
                    id = 'histo_dropdown',
                    options=[
                        {'label': 'Histogramme Types 1&2', 'value': 'type12'},
                        {'label': 'Histogramme des Types', 'value': 'types'}
                    ],
                    value = 'type12',
                    clearable=False,
                    style = {"font-weight":"bold",'border-radius' : '10px','font-family' : 'sans-serif','background-color' : '#FFDE00'}
                ),
                
                html.Div(children=[
                    dcc.Graph(
                        id="histo_graph",
                        figure = types_histo('Type','Types')
                    ),
                ],
                
                style={'textAlign': 'center', 'height' : '700', 'font-family' : 'sans-serif'}
                ),
                html.H3(
                    id = 'histo_title',
                    children=f'Nombres des différents types en fonction de tous les Types',
                    style={'textAlign': 'center', 'font-family' : 'sans-serif' }
                ),
                   
                    
                
            ],
            style={'display':'inline-block','height' : '700', 'width' : '750','text-align' : 'center','background-color' : '#F5F5F5'}
        ),
        #
        #Histo                                  ##################
        #


        #
        #Pokedex                                ##################
        #
        html.Div(
            children=[
                html.H1(
                    children=f'Pokédex',
                    style={'textAlign': 'center','font-family' : 'sans-serif', 'background-color' : '#e4000f', 'color' : 'white' , 'margin' :'0', 'padding' : '10px 0px'}
                ),

                #
                #Choix Pokémon Gauche           ##################
                #

                html.Div(
                    children=[
                        html.H3(
                            id='id_left',
                            children=f'N° de Pokédex : {id_left} ',
                            style = {'text-align' : 'center', 'font-family' : 'sans-serif','margin' : '0', 'padding' : '5px'}
                        ),
                        html.Img( 
                            id = 'pokemon_sprite_left',
                            src= display_sprite(0),
                        ),
                        dcc.Dropdown(
                            id = 'pokemon_dropdown_left',
                            options=dd1_pokemon_list,
                            value = dd1_pokemon_list[0]['value'],
                            clearable=False,
                            style = {"font-weight":"bold","background-color":"#6495ED", 'border-radius' : '10px','font-family' : 'sans-serif'}
                        ),
                        html.Img( 
                            id = 'pokemon_png_left',
                            src= display_img(0),
                            height = 150,
                            width = 150,
                            style = {
                                'padding' : '50px'
                            }
                        ),
                        html.H4(
                            id = 'region_left',
                            children=f'Région : {region_left} ',
                            style = {'text-align' : 'center', 'font-family' : 'sans-serif','margin' : '0', 'padding' : '5px'}
                        ),
                        html.Img( 
                            id = 'pokemon_type1_left',
                            src= display_type('grass.png'),
                            style = {
                                'display':'inline-block'
                            }
                        ),
                        html.Img( 
                            id = 'pokemon_type2_left',
                            src= display_type('poison.png'),
                            style = {
                                'display':'inline-block'
                            }
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='stats_bar_left',
                                    figure = stats_bar(0)
                                )
                            ],
                        )
                        
                    ],
                    className="box1",
                    style={
                        'text-align' : 'center',
                        'display':'inline-block',
                        'height' : '800', 'width' : '341'
                    }
                ),

                #
                #Choix Pokémon Gauche           ##################
                #

                #
                #Polar Chart Stats Pokémon      ##################
                #

                html.Div(
                    children=[
                        dcc.Graph(
                            id='stats_graph',
                            figure = stats_graph(0,3),
                            style ={'font-family' : 'sans-serif'}
                        )
                    ],
                    className="box2",
                    style={
                        
                        'display':'inline-block',
                        'position' : 'relative'
                    }
                ),

                #
                #Polar Chart Stats Pokémon      ##################
                #

                #
                #Choix Pokémon Droit            ##################
                #
                html.Div(
                    children=[
                        html.H3(
                            id = 'id_right',
                            children=f'N° de Pokédex : {id_right} ',
                            style = {'text-align' : 'center', 'font-family' : 'sans-serif','margin' : '0', 'padding' : '5px'}
                        ),
                        html.Img( 
                            id = 'pokemon_sprite_right',
                            src= display_sprite(3),
                        ),
                        dcc.Dropdown(
                            id = 'pokemon_dropdown_right',
                            options=dd1_pokemon_list,
                            value = dd1_pokemon_list[3]['value'],
                            clearable=False,
                            style = {
                                "font-weight":"bold",
                                "background-color":"salmon", 
                                'border-radius' : '10px',
                                'font-family' : 'sans-serif'
                            }
                        ),
                        html.Img( 
                            id = 'pokemon_png_right',
                            src= display_img(3),
                            height = 150,
                            width = 150,
                            style = {
                                'padding' : '50px'
                            }
                        ),
                        html.H4(
                            id='region_right',
                            children=f'Région : {region_right} ',
                            style = {'text-align' : 'center', 'font-family' : 'sans-serif','margin' : '0', 'padding' : '5px'}
                        ),
                        html.Img( 
                            id = 'pokemon_type1_right',
                            src= display_type('fire.png'),
                            style = {
                                'display':'inline-block'
                            }
                        ),
                        html.Img( 
                            id = 'pokemon_type2_right',
                            src= display_type('fire.png'),
                            style = {
                                'display':'none'
                            }
                        ),
                        html.Div(
                            children=[
                                dcc.Graph(
                                    id='stats_bar_right',
                                    figure = stats_bar(3)
                                )
                            ],
                        )

                    ],
                    className="box3",
                    style={
                        'text-align' : 'center',
                        'display':'inline-block',
                        'height' : '800', 'width' : '341'
                    }
                ),
                #
                #Choix Pokémon Droit            ##################
                #

            ],
            style={
                'position' : 'relative',
                'display':'inline-block',
                'height' : 'auto', 
                'width' : 'auto',
                'background-color' : '#F5F5F5'
            }
                
        ),

        #
        #Pokedex                                ##################
        #
        

        ],
        style = {
            'background-color' : '#F5F5F5','margin' : '0', 'width' : '1500px', 'text-align' : 'center'
        }
    )


    #############               CallBack                ##############

    #############               Geo Graph               ##############

    #
    #Met à jour la figure géographique en fonction des Inputs du Dropdown          #############
    #

    @app.callback(
    Output(component_id='map_graph', component_property='figure'), 
    [Input(component_id='map_dropdown', component_property='value')]
    )
    def update_map(input_value): 
        """
        Retourne la figure géographique en fonction de la valeur du dropdown

        Args:
            input_value

        Returns:
            update_map(input_value) : map_graph(..)
        """
        if(input_value == "region"): return map_graph(input_value)
        if(input_value == "type1"): return map_graph(first_type)
        if(input_value == "type2"): return map_graph(second_type)

    #
    #Met à jour le titre de la figure géographique en fonction des Inputs du Dropdown          #############
    #

    @app.callback(
    Output(component_id='map_title', component_property='children'), 
    [Input(component_id='map_dropdown', component_property='value')]
    )
    def update_map_title(input_value): 
        """
        Retourne le nom de la figure géographique en fonction de la valeur du dropdown

        Args:
            input_value

        Returns:
            update_map_title(input_value) : 'title...'
        """
        if(input_value == "region"): return 'Carte des Régions '
        if(input_value == "type1"): return 'Carte des Pokémons filtré par types 1 '
        if(input_value == "type2"): return 'Carte des Pokémons filtré par types 2 '




    #############               Histo                  ##############



    #
    #Met à jour la figure géographique en fonction des Inputs du Dropdown          #############
    #

    @app.callback(
    Output(component_id='histo_graph', component_property='figure'), 
    [Input(component_id='histo_dropdown', component_property='value')]
    )
    def update_histo(input_value): 
        """
        Retourne l'histogramme en fonction de la valeur du dropdown

        Args:
            input_value

        Returns:
            update_histo(input_value) : types_histo(..)
        """
        if(input_value == "types"): return types_histo("Types","Type")
        if(input_value == "type12"): return types_histo('Type','Types')

    #
    #Met à jour le titre de la figure géographique en fonction des Inputs du Dropdown          #############
    #

    @app.callback(
    Output(component_id='histo_title', component_property='children'), 
    [Input(component_id='histo_dropdown', component_property='value')]
    )
    def update_histo_title(input_value): 
        """
        Retourne le nom de l'histogramme en fonction de la valeur du dropdown

        Args:
            input_value

        Returns:
            update_histo_title(input_value) : 'title...'
        """
        if(input_value == "type12"): return 'Nombres des différents types en fonction de tous les Types'
        if(input_value == "types"): return 'Nombres des différents types en fonction du Type 1 et Type 2'




    #############               Pokédex               ##############

    #########           Update Left Pokemon ID          ############
    @app.callback(
    Output(component_id='id_left', component_property='children'),
    [Input(component_id='pokemon_dropdown_left', component_property='value')])

    def update_left_id(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        if input_value < 10 : zero = '00'
        elif input_value >= 10 and input_value < 100 : zero = '0'
        else : zero = ''
        return f'N° de Pokédex : {zero}{input_value} '

    #########           Update Right Pokemon ID          ############
    @app.callback(
    Output(component_id='id_right', component_property='children'),
    [Input(component_id='pokemon_dropdown_right', component_property='value')])

    def update_right_id(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        if input_value < 10 : zero = '00'
        elif input_value >= 10 and input_value < 100 : zero = '0'
        else : zero = ''
        return f'N° de Pokédex : {zero}{input_value} '



    #########           Update Left Pokemon Region          ############
    @app.callback(
    Output(component_id='region_left', component_property='children'),
    [Input(component_id='pokemon_dropdown_left', component_property='value')])

    def update_left_id(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        return f'Région : {pokemon_location["region"][input_value - 1]} '



    #########           Update Right Pokemon Region          ############
    @app.callback(
    Output(component_id='region_right', component_property='children'),
    [Input(component_id='pokemon_dropdown_right', component_property='value')])

    def update_left_id(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        return f'Région : {pokemon_location["region"][input_value - 1]} '



    #
    #Mise à jour du type 1 du Pokémon de droite         #############
    #

    @app.callback(
    Output(component_id='pokemon_type1_right', component_property='src'),
    [Input(component_id='pokemon_dropdown_right', component_property='value')])

    def update_right_pkm_type1(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        src = select_type1(input_value)
        return src

    #
    #Mise à jour du type 2 du Pokémon de droite         #############
    #

    @app.callback(
    [Output(component_id='pokemon_type2_right', component_property='src'),
    Output(component_id='pokemon_type2_right', component_property='style')],
    [Input(component_id='pokemon_dropdown_right', component_property='value')])

    def update_right_pkm_type2(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src, {'display' : 'inline-block'} if second_type != null
            update_right_pkm_type1(input_value) : src, {'display' : 'none'} if second_type == null

        """
        if second_type[input_value-1] != 'null' : 
            src = select_type2(input_value)
            style = {'display' : 'inline-block'}
        else : 
            src = select_type1(input_value)
            style = {'display': 'none'}
        return src, style

    #
    #Mise à jour du type 1 du Pokémon de gauche         #############
    #

    @app.callback(
    Output(component_id='pokemon_type1_left', component_property='src'),
    [Input(component_id='pokemon_dropdown_left', component_property='value')])

    def update_left_pkm_type1(input_value):
        """
        Retourne l'image du type 1 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type1(input_value) : src
        """
        src = select_type1(input_value)
        return src

    #
    #Mise à jour du type 2 du Pokémon de gauche         #############
    #

    @app.callback(
    [Output(component_id='pokemon_type2_left', component_property='src'),
    Output(component_id='pokemon_type2_left', component_property='style')],
    [Input(component_id='pokemon_dropdown_left', component_property='value')])

    def update_left_pkm_type2(input_value):
        """
        Retourne l'image du type 2 correspondant au Pokémon

        Args:
            input_value

        Returns:
            update_right_pkm_type2(input_value) : src, {'display' : 'inline-block'} if second_type != null
            update_right_pkm_type2(input_value) : src, {'display' : 'none'} if second_type == null

        """
        if second_type[input_value-1] != 'null' : 
            src = select_type2(input_value)
            style = {'display' : 'inline-block'}
        else : 
            src = select_type1(input_value)
            style = {'display': 'none'}
        return src, style


    #
    #Déroulant update image gauche et petit easter egg pour le Pokémon n°132 (Métamorphe)         #############
    #

    @app.callback(
    Output(component_id='pokemon_png_left', component_property='src'), 
    Input(component_id='pokemon_dropdown_left', component_property='value'),
    Input(component_id='pokemon_dropdown_right', component_property='value') 
    )

    def update_pokemon_png(pokemon_dropdown_left,pokemon_dropdown_right): 
        """
        Retourne l'image du pokemon de gauche

        Args:
            pokemon_dropdown_left,pokemon_dropdown_right

        Returns:
            update_pokemon_png(pokemon_dropdown_left,pokemon_dropdown_right) : display_img(..) 
        """
        if(pokemon_dropdown_left == 132): return display_img(pokemon_dropdown_right -1)
        return display_img(pokemon_dropdown_left - 1)

    #
    #Déroulant update image droite et petit easter egg pour le Pokémon n°132 (Métamorphe)         #############
    #

    @app.callback(
    Output(component_id='pokemon_png_right', component_property='src'), 
    Input(component_id='pokemon_dropdown_left', component_property='value'),
    Input(component_id='pokemon_dropdown_right', component_property='value') 
    )

    def update_pokemon_png(pokemon_dropdown_left,pokemon_dropdown_right): 
        """
        Retourne l'image du pokemon de droite

        Args:
            pokemon_dropdown_left,pokemon_dropdown_right

        Returns:
            update_pokemon_png(pokemon_dropdown_left,pokemon_dropdown_right) : display_img(..) 
        """
        if(pokemon_dropdown_right == 132): return display_img(pokemon_dropdown_left -1)
        return display_img(pokemon_dropdown_right - 1)

    #
    #Déroulant update sprite gauche et petit easter egg pour le Pokémon n°132 (Métamorphe)         #############
    #

    @app.callback(
    Output(component_id='pokemon_sprite_left', component_property='src'), 
    Input(component_id='pokemon_dropdown_left', component_property='value'),
    Input(component_id='pokemon_dropdown_right', component_property='value') 
    )

    def update_pokemon_sprite(pokemon_dropdown_left,pokemon_dropdown_right): 
        """
        Retourne le sprite du pokemon de gauche

        Args:
            pokemon_dropdown_left,pokemon_dropdown_right

        Returns:
            update_pokemon_sprite(pokemon_dropdown_left,pokemon_dropdown_right) : display_sprite(..) 
        """
        if(pokemon_dropdown_left == 132): return display_sprite(pokemon_dropdown_right -1)
        return display_sprite(pokemon_dropdown_left - 1)

    #
    #Déroulant update sprite droite et petit easter egg pour le Pokémon n°132 (Métamorphe)         #############
    #

    @app.callback(
    Output(component_id='pokemon_sprite_right', component_property='src'), 
    Input(component_id='pokemon_dropdown_left', component_property='value'),
    Input(component_id='pokemon_dropdown_right', component_property='value') 
    )

    def update_pokemon_sprite(pokemon_dropdown_left,pokemon_dropdown_right): 
        """
        Retourne le sprite du pokemon de droite

        Args:
            pokemon_dropdown_left,pokemon_dropdown_right

        Returns:
            update_pokemon_sprite(pokemon_dropdown_left,pokemon_dropdown_right) : display_sprite(..) 
        """
        if(pokemon_dropdown_right == 132): return display_sprite(pokemon_dropdown_left -1)
        return display_sprite(pokemon_dropdown_right - 1)
    

    #
    #Update du polar chart (comparaison des stats)         #############
    #

    @app.callback(
    Output('stats_graph', 'figure'), # (1)
    Input('pokemon_dropdown_left', 'value'),
    Input('pokemon_dropdown_right', 'value') 
    )

    def update_stats_graph(pokemon_dropdown_left, pokemon_dropdown_right):
        """
        Retourne les stats sur le polar chart

        Args:
            pokemon_dropdown_left, pokemon_dropdown_right

        Returns:
            update_stats_graph(pokemon_dropdown_left, pokemon_dropdown_right) : stats_graph(..)
        """ 
        return stats_graph(pokemon_dropdown_left-1,pokemon_dropdown_right-1)

    #
    #Update bar stats gauche          #############
    #

    @app.callback(
    Output('stats_bar_left', 'figure'), 
    [Input('pokemon_dropdown_left', 'value')]
    )

    def update_stats_bar(pokemon_dropdown_left):
        """
        Retourne les stats du pokemon de gauche

        Args:
            pokemon_dropdown_left

        Returns:
            update_stats_bar(pokemon_dropdown_left) : stats_bar(..)
        """ 
        return stats_bar(pokemon_dropdown_left-1)

    #
    #Update bar stats droit          #############
    #

    @app.callback(
    Output('stats_bar_right', 'figure'), 
    [Input('pokemon_dropdown_right', 'value')]
    )

    def update_stats_bar(pokemon_dropdown_right):
        """
        Retourne les stats du pokemon de droite

        Args:
            pokemon_dropdown_right

        Returns:
            update_stats_bar(pokemon_dropdown_right) : stats_bar(..)
        """ 
        return stats_bar(pokemon_dropdown_right-1)

    #
    # RUN APP                               #############
    #

    app.run_server(debug=True) 