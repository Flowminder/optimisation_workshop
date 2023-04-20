import leafmap.foliumap as leafmap
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.lines as lines
from matplotlib.ticker import MaxNLocator

### functions for wdf_workshop notebook to reduce the amount of code in the notebook.
### workshop_map and coverage_table are NOT currently fully generic so need adapting for use in other optimisation projects.


# function for creating Kaduna default map with boundary and population
def workshop_map(title, boundary, population):
    
    workshop_map = leafmap.Map(center=(10.48650018, 7.42406665), 
                     zoom=8,
                     draw_control=False,
                     measure_control=False,
                     fullscreen_control=False,
                     attribution_control=True,)
    
    # add basemap
    workshop_map.add_basemap('CartoDB.Positron')
    
    # add boundary to map
    workshop_map.add_gdf(boundary, layer_name = 'Kaduna boundary', 
                         style ={'fillColor': 'none', 'color': '#CBA45A', 'weight': 1})
    
    # add the population raster
    workshop_map.add_raster(population, palette='YlGn_r', layer_name='Kaduna population')
    
    # add colorbar
    image = 'https://i.imgur.com/aIb0Ygm.png'
    workshop_map.add_image(image, position='topleft')
    
    # add title
    workshop_map.add_title(title, font_size='20px', align='center')
    
    return workshop_map


# Generic function for plotting coverage and extra people added by new sites. If priority 2 and priority 3 are defined,
# a dividing line and annotations will be added
def coverage_graph(new_sites, title):
    
    fig, axs = plt.subplots(2, figsize=(10, 7))
    fig.suptitle(title)
    
    # % population covered
    axs[0].plot(new_sites['site_rank'], (new_sites['cumulative_perc_covered']), color = '#095798')
    axs[0].set(xlabel='New sites added in rank order', ylabel='Total % population covered')
    axs[0].xaxis.set_major_locator(MaxNLocator(integer=True))
    axs[0].tick_params(axis='both', which='both', labelsize=8)
    axs[0].title.set_text('Coverage as new sites are added')
        
    # Population covered
    axs[1].bar(new_sites['site_rank'], new_sites['extra_people_covered'], color = '#095798', width=10)
    axs[1].set(xlabel='New sites added in rank order', ylabel= 'Estimated population covered by site')
    axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    axs[1].tick_params(axis='both', which='both', labelsize=8)
    axs[1].title.set_text('Estimated population served by each site')
    
    if 'priority' in new_sites.columns:
        
            p2_sites = new_sites.loc[new_sites['priority'] == 'priority 2']
            p3_sites = new_sites.loc[new_sites['priority'] == 'priority 3']
            p2_sites_coverage = p2_sites.iloc[[-1]].cumulative_perc_covered.values[0]
            
            # add horizontal line to first graph
            axs[0].add_line(lines.Line2D([0, max(p2_sites.site_rank.values)], 
                                 [p2_sites_coverage, p2_sites_coverage], 
                                 linestyle = '--', color="#701F53"))

            # add vertical line to first graph
            axs[0].add_line(lines.Line2D([max(p2_sites.site_rank.values), max(p2_sites.site_rank.values)], 
                                 [40, p2_sites_coverage], 
                                 linestyle = '--', color="#701F53"))
            
            # add p2 label to first graph
            axs[0].annotate('P2\nsites', xy =(max(p2_sites.site_rank.values) - 250, max(p2_sites.cumulative_perc_covered.values)*0.75)) 
            
            # add p3 label to first graph
            axs[0].annotate('P3\nsites', xy =(max(p2_sites.site_rank.values) + 50, max(p2_sites.cumulative_perc_covered.values)*0.75)) 
            
            # add vertical line to second graph
            axs[1].add_line(lines.Line2D([max(p2_sites.site_rank.values), max(p2_sites.site_rank.values)], 
                                 [0, max(new_sites.extra_people_covered.values)], 
                                 linestyle = '--', color="#701F53"))
            
            # add p2 label to second graph
            axs[1].annotate('P2\nsites', xy =(max(p2_sites.site_rank.values) - 250, max(p2_sites.extra_people_covered.values)/2)) 
            
            # add p3 label to second graph
            axs[1].annotate('P3\nsites', xy =(max(p2_sites.site_rank.values) + 50, max(p2_sites.extra_people_covered.values)/2)) 
            

    fig.tight_layout()
    
# function for producing a coverage table showing increased coverage statistics   
def coverage_table(existing_sites, p2_sites, p3_sites):
    
    d = {'Priority levels': ['P1 (existing sites)', 'P1 + P2', 'P1 + P2 + P3'], 
     'Number of sites': [len(existing_sites), len(existing_sites) + len(p2_sites), len(kaduna_existing_sites) + len(p2_sites) + len(p3_sites)],
     'Estimated population covered': [4247042, 4247042 + sum(p2_sites.extra_people_covered), 4247042 + sum(p2_sites.extra_people_covered) + sum(p3_sites.extra_people_covered)],
     'Estimated % population covered': [39, p2_sites.iloc[[-1]].cumulative_perc_covered.values[0], p3_sites.iloc[[-1]].cumulative_perc_covered.values[0]]}
    
    
    df = pd.DataFrame(data=d)
    
    return df