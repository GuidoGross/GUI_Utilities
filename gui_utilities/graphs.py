from .format import decimal_format
from .system import in_google_colaboratory
import matplotlib.colors as colors
import matplotlib.pyplot as pyplot
import numpy
import pandas
import os
if not in_google_colaboratory(): from PyQt6 import QtGui
from mpl_toolkits.axes_grid1 import make_axes_locatable

def _configure_graph_window(manager, window_title, maximize_window, icon_path):
    if in_google_colaboratory(): return
    if hasattr(manager, "set_window_title"): manager.set_window_title(window_title)
    window = getattr(manager, "window", None)
    if window is None: return
    if maximize_window and hasattr(window, "showMaximized"): window.showMaximized()
    if icon_path and os.path.exists(icon_path) and hasattr(window, "setWindowIcon"):
        window.setWindowIcon(QtGui.QIcon(icon_path))

def _resolve_color_palette(color_palette, base_color, color_saturation_range, color_value_range, colors_number, continuous = False):
    def _build_color_list():
        if color_palette is None:
            hue, _, _ = colors.rgb_to_hsv(colors.to_rgb(base_color))
            minimum_saturation, maximum_saturation = color_saturation_range
            minimum_value, maximum_value = color_value_range
            return [
                colors.to_hex(colors.hsv_to_rgb((
                    hue,
                    maximum_saturation - (i / colors_number) * (maximum_saturation - minimum_saturation),
                    minimum_value + (i / colors_number) * (maximum_value - minimum_value)
                )))
                for i in range(colors_number)
            ]
        if isinstance(color_palette, colors.Colormap): colormap = color_palette
        elif isinstance(color_palette, str) and color_palette in pyplot.colormaps():
            colormap = pyplot.get_cmap(color_palette)
        elif isinstance(color_palette, (list, tuple, numpy.ndarray)): return list(color_palette)
        elif colors.is_color_like(color_palette):
            return [colors.to_hex(colors.to_rgb(color_palette)) for _ in range(colors_number)]
        else: return color_palette
        if colors_number <= 1: return [colors.to_hex(colormap(0.5))]
        return [colors.to_hex(colormap(i / (colors_number - 1))) for i in range(colors_number)]

    resolved_color_palette = _build_color_list()
    if continuous and isinstance(resolved_color_palette, (list, tuple, numpy.ndarray)):
        return colors.LinearSegmentedColormap.from_list("custom_color_palette", list(resolved_color_palette))
    return resolved_color_palette

def _resolve_histogram_bins(bins, data):
    if bins != "sturges": return bins
    clean_data = pandas.Series(data).dropna().to_numpy(dtype = float)
    if len(clean_data) == 0: return bins
    distinct_values_count = len(numpy.unique(clean_data))
    minimum_intervals = min(5, distinct_values_count)
    sturges_bins_edges = numpy.histogram_bin_edges(clean_data, bins = "sturges")
    sturges_intervals = min(len(sturges_bins_edges) - 1, distinct_values_count)
    if sturges_intervals <= 0: return sturges_bins_edges
    minimum_edge = int(numpy.floor(clean_data.min()))
    maximum_edge = int(numpy.ceil(clean_data.max()))
    if minimum_edge == maximum_edge: return sturges_bins_edges
    integer_bins_edges = numpy.unique(numpy.linspace(minimum_edge, maximum_edge, sturges_intervals + 1).round().astype(int))
    if len(integer_bins_edges) - 1 >= minimum_intervals: return integer_bins_edges
    decimal_intervals = min(max(sturges_intervals, minimum_intervals), distinct_values_count)
    return numpy.histogram_bin_edges(clean_data, bins = decimal_intervals)

def bar_chart(
    variable,
    counts,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    x_label = None,
    y_label = None,
    labels_font_size = 12,
    labels_font_weight = "normal",
    labels_padding = 10,
    base_color = "#00bfff",
    bar_orientation = "vertical",
    bars_width = 0.75,
    bars_alignment = "center",
    bars_edge_color = "none",
    bars_line_width = 0,
    bars_alpha = 1.0,
    show_grid = True,
    grid_axis = "y",
    grid_color = "#ffffff",
    grid_line_style = "--",
    grid_line_width = 0.5,
    grid_alpha = 0.5,
    x_ticks = None,
    y_ticks = None,
    x_tick_labels = None,
    y_tick_labels = None,
    ticks_font_size = 10,
    ticks_rotation = 0,
    x_limit = None,
    y_limit = None,
    x_margin = 0,
    y_margin = 0,
    spines_visible = (False, False, True, True),
    show_legend = False,
    legend_reverse_order = False,
    legend_location = "best",
    legend_bbox_to_anchor = None,
    legend_frame = False,
    legend_edge_color = None,
    legend_background_color = None,
    layout_padding = 2.5,
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    n = len(counts)
    match bar_orientation:
        case "vertical":
            bars = axes.bar(
                counts.index if hasattr(counts, "index") else range(n),
                counts.values if hasattr(counts, "values") else counts,
                width = bars_width,
                align = bars_alignment,
                color = base_color,
                edgecolor = bars_edge_color,
                linewidth = bars_line_width,
                alpha = bars_alpha,
            )
        case "horizontal":
            bars = axes.barh(
                counts.index if hasattr(counts, "index") else range(n),
                counts.values if hasattr(counts, "values") else counts,
                height = bars_width,
                align = bars_alignment,
                color = base_color,
                edgecolor = bars_edge_color,
                linewidth = bars_line_width,
                alpha = bars_alpha,
            )
    axes.set_xlabel(x_label if x_label is not None else variable, fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    axes.set_ylabel(y_label if y_label is not None else "Frecuencia", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    if show_grid:
        axes.grid(
            visible = True,
            axis = grid_axis,
            color = grid_color,
            linestyle = grid_line_style,
            linewidth = grid_line_width,
            alpha = grid_alpha
        )
    if x_ticks is not None: axes.set_xticks(x_ticks)
    if y_ticks is not None: axes.set_yticks(y_ticks)
    if x_tick_labels is not None: axes.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: axes.set_yticklabels(y_tick_labels)
    axes.tick_params(axis = "both", labelsize = ticks_font_size, rotation = ticks_rotation)
    if x_limit is not None: axes.set_xlim(x_limit)
    if y_limit is not None: axes.set_ylim(y_limit)
    axes.margins(x = x_margin, y = y_margin)
    axes.spines["top"].set_visible(spines_visible[0])
    axes.spines["right"].set_visible(spines_visible[1])
    axes.spines["bottom"].set_visible(spines_visible[2])
    axes.spines["left"].set_visible(spines_visible[3])
    if show_legend:
        handles, labels = (bars[::-1], (counts.index[::-1] if hasattr(counts, "index") else range(n)[::-1])) if legend_reverse_order else (bars, (counts.index if hasattr(counts, "index") else range(n)))
        axes.legend(
            handles,
            labels,
            loc = legend_location,
            bbox_to_anchor = legend_bbox_to_anchor,
            frameon = legend_frame,
            edgecolor = legend_edge_color,
            facecolor = legend_background_color
        )
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def pie_chart(
    variable,
    counts,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    color_palette = None,
    base_color = "#00bfff",
    color_saturation_range = (0.75, 1.0),
    color_value_range = (0.25, 0.75),
    show_labels = True,
    percentage_decimals = 2,
    show_percentages = True,
    labels_distance = 1.1,
    porcentages_distance = 0.55,
    start_angle = 90,
    counter_clock = False,
    wedges_edge_color = "none",
    wedges_line_width = 0,
    radius = 1.0,
    explode = None,
    shadow = False,
    labels_font_size = None,
    labels_rotation = True,
    labels_horizontal_alignment = "automatic",
    labels_vertical_alignment = "automatic",
    porcentages_font_size = None,
    show_legend = False,
    legend_reverse_order = False,
    legend_location = "best",
    legend_bbox_to_anchor = (1, 1),
    legend_frame = False,
    legend_edge_color = None,
    legend_background_color = None,
    layout_padding = 2.5,
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    n = len(counts)
    color_list = _resolve_color_palette(
        color_palette,
        base_color,
        color_saturation_range,
        color_value_range,
        n
    )
    wedges, label_texts, porcentage_texts = axes.pie(
        counts,
        labels = counts.index if show_labels else None,
        autopct = (lambda percentage: f"{decimal_format(percentage, percentage_decimals)}%") if show_percentages else None,
        colors = color_list,
        labeldistance = labels_distance,
        pctdistance = porcentages_distance,
        startangle = start_angle,
        counterclock = counter_clock,
        wedgeprops = {"edgecolor": wedges_edge_color, "linewidth": wedges_line_width},
        radius = radius,
        explode = explode,
        shadow = shadow,
    )
    if labels_font_size is not None:
        for text in label_texts: text.set_fontsize(labels_font_size)
    for wedge, text in zip(wedges, label_texts):
        angle = (wedge.theta2 + wedge.theta1) / 2
        angle %= 360
        if labels_rotation:
            rotation = angle - 90 if 0 <= angle <= 180 else angle + 90
            text.set_rotation(rotation)
        else:
            if labels_horizontal_alignment == "automatic":
                if (45 <= angle <= 135) or (225 <= angle <= 315): horizontal_alignment = "center"
                elif 135 < angle < 225: horizontal_alignment = "right"
                else: horizontal_alignment = "left"
                text.set_horizontalalignment(horizontal_alignment)
            else: text.set_horizontalalignment(labels_horizontal_alignment)
            if labels_vertical_alignment == "automatic":
                if 45 <= angle <= 135: vertical_alignment = "bottom"
                elif 225 <= angle <= 315: vertical_alignment = "top"
                else: vertical_alignment = "center"
                text.set_verticalalignment(vertical_alignment)
            else: text.set_verticalalignment(labels_vertical_alignment)
    if porcentages_font_size is not None and show_percentages:
        for text in porcentage_texts: text.set_fontsize(porcentages_font_size)
    if show_legend:
        handles, labels = (wedges[::-1], counts.index[::-1]) if not legend_reverse_order else (wedges, counts.index)
        axes.legend(
            handles,
            labels,
            loc = legend_location,
            bbox_to_anchor = legend_bbox_to_anchor,
            frameon = legend_frame,
            edgecolor = legend_edge_color,
            facecolor = legend_background_color
        )
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def histogram(
    variable,
    data,
    bins = "sturges",
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    x_label = None,
    y_label = None,
    labels_font_size = 12,
    labels_font_weight = "normal",
    labels_padding = 10,
    base_color = "#00bfff",
    show_bars = True,
    show_line = False,
    histogram_type = "bar",
    alignment = "mid",
    orientation = "vertical",
    bars_relative_width = 1,
    use_logaritmic_scale = False,
    bars_edge_color = "#ffffff",
    bars_line_width = 0.5,
    bars_alpha = 1.0,
    line_color = None,
    line_style = "-",
    line_width = 2,
    line_alpha = 1.0,
    markers = "o",
    markers_size = 8,
    markers_edge_color = "#ffffff",
    markers_background_color = None,
    show_grid = True,
    grid_axis = "y",
    grid_color = "#ffffff",
    grid_line_style = "--",
    grid_line_width = 0.5,
    grid_alpha = 0.5,
    x_ticks = None,
    y_ticks = None,
    x_tick_labels = None,
    y_tick_labels = None,
    ticks_font_size = 10,
    ticks_rotation = 0,
    x_limit = None,
    y_limit = None,
    x_margin = 0,
    y_margin = 0,
    spines_visible = (False, False, True, True),
    show_legend = False,
    legend_label = None,
    legend_location = "best",
    legend_bbox_to_anchor = None,
    legend_frame = False,
    legend_edge_color = None,
    legend_background_color = None,
    layout_padding = 2.5,
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    resolved_bins = _resolve_histogram_bins(bins, data)
    counts, bins_edges, patches = axes.hist(
        data,
        bins = resolved_bins,
        color = base_color,
        histtype = histogram_type,
        align = alignment,
        orientation = orientation,
        rwidth = bars_relative_width,
        log = use_logaritmic_scale,
        edgecolor = bars_edge_color,
        linewidth = bars_line_width,
        alpha = bars_alpha if show_bars else 0,
        label = legend_label if legend_label is not None else variable
    )
    midpoints = 0.5 * (bins_edges[1:] + bins_edges[:-1])
    interval_labels_decimals = None if numpy.allclose(bins_edges, numpy.round(bins_edges)) else 6
    interval_labels = [
        f"{'[' if interval_index == 0 else '('}{decimal_format(round(lower_edge, 6), interval_labels_decimals)}; "
        f"{decimal_format(round(upper_edge, 6), interval_labels_decimals)}]"
        for interval_index, (lower_edge, upper_edge) in enumerate(zip(bins_edges[:-1], bins_edges[1:]))
    ]
    if show_line:
        axes.plot(
            midpoints,
            counts,
            color = line_color if line_color is not None else base_color,
            linestyle = line_style,
            linewidth = line_width,
            alpha = line_alpha,
            marker = markers,
            markersize = markers_size,
            markeredgecolor = markers_edge_color,
            markerfacecolor = markers_background_color if markers_background_color is not None else (line_color if line_color is not None else base_color),
            label = legend_label if legend_label is not None and not show_bars else (None if show_bars else variable)
        )
    if show_bars:
        if orientation == "vertical" and x_ticks is None and x_tick_labels is None:
            axes.set_xticks(midpoints)
            axes.set_xticklabels(interval_labels)
        if orientation == "horizontal" and y_ticks is None and y_tick_labels is None:
            axes.set_yticks(midpoints)
            axes.set_yticklabels(interval_labels)
    axes.set_xlabel(x_label if x_label is not None else variable, fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    axes.set_ylabel(y_label if y_label is not None else "Frecuencia", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    if show_grid:
        axes.grid(
            visible = True,
            axis = grid_axis,
            color = grid_color,
            linestyle = grid_line_style,
            linewidth = grid_line_width,
            alpha = grid_alpha
        )
    if x_ticks is not None: axes.set_xticks(x_ticks)
    if y_ticks is not None: axes.set_yticks(y_ticks)
    if x_tick_labels is not None: axes.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: axes.set_yticklabels(y_tick_labels)
    axes.tick_params(axis = "both", labelsize = ticks_font_size, rotation = ticks_rotation)
    if x_limit is not None: axes.set_xlim(x_limit)
    if y_limit is not None: axes.set_ylim(y_limit)
    axes.margins(x = x_margin, y = y_margin)
    axes.spines["top"].set_visible(spines_visible[0])
    axes.spines["right"].set_visible(spines_visible[1])
    axes.spines["bottom"].set_visible(spines_visible[2])
    axes.spines["left"].set_visible(spines_visible[3])
    if show_legend:
        axes.legend(
            loc = legend_location,
            bbox_to_anchor = legend_bbox_to_anchor,
            frameon = legend_frame,
            edgecolor = legend_edge_color,
            facecolor = legend_background_color
        )
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def line_chart(
    variable,
    x,
    y,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    x_label = None,
    y_label = None,
    labels_font_size = 12,
    labels_font_weight = "normal",
    labels_padding = 10,
    base_color = "#00bfff",
    line_width = 2,
    line_style = "-",
    line_alpha = 1.0,
    show_area = False,
    area_alpha = 0.25,
    markers = "o",
    markers_size = 6,
    markers_edge_color = "#ffffff",
    markers_background_color = None,
    show_grid = True,
    grid_axis = "both",
    grid_color = "#ffffff",
    grid_line_style = "--",
    grid_line_width = 0.5,
    grid_alpha = 0.5,
    x_ticks = None,
    y_ticks = None,
    x_tick_labels = None,
    y_tick_labels = None,
    ticks_font_size = 10,
    ticks_rotation = 0,
    x_limit = None,
    y_limit = None,
    x_margin = 0,
    y_margin = 0,
    spines_visible = (False, False, True, True),
    show_legend = False,
    legend_label = None,
    legend_location = "best",
    legend_bbox_to_anchor = None,
    legend_frame = False,
    legend_edge_color = None,
    legend_background_color = None,
    layout_padding = 2.5,
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    if show_area: axes.fill_between(x, y, color = base_color, alpha = area_alpha)
    line, = axes.plot(
        x,
        y,
        color = base_color,
        linewidth = line_width,
        linestyle = line_style,
        alpha = line_alpha,
        marker = markers,
        markersize = markers_size,
        markeredgecolor = markers_edge_color,
        markerfacecolor = markers_background_color if markers_background_color is not None else base_color,
        label = legend_label if legend_label is not None else variable
    )
    axes.set_xlabel(x_label if x_label is not None else variable, fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    axes.set_ylabel(y_label if y_label is not None else "Valor", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    if show_grid:
        axes.grid(
            visible = True,
            axis = grid_axis,
            color = grid_color,
            linestyle = grid_line_style,
            linewidth = grid_line_width,
            alpha = grid_alpha
        )
    if x_ticks is not None: axes.set_xticks(x_ticks)
    if y_ticks is not None: axes.set_yticks(y_ticks)
    if x_tick_labels is not None: axes.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: axes.set_yticklabels(y_tick_labels)
    axes.tick_params(axis = "both", labelsize = ticks_font_size, rotation = ticks_rotation)
    if x_limit is not None: axes.set_xlim(x_limit)
    if y_limit is not None: axes.set_ylim(y_limit)
    axes.margins(x = x_margin, y = y_margin)
    axes.spines["top"].set_visible(spines_visible[0])
    axes.spines["right"].set_visible(spines_visible[1])
    axes.spines["bottom"].set_visible(spines_visible[2])
    axes.spines["left"].set_visible(spines_visible[3])
    if show_legend:
        axes.legend(
            loc = legend_location,
            bbox_to_anchor = legend_bbox_to_anchor,
            frameon = legend_frame,
            edgecolor = legend_edge_color,
            facecolor = legend_background_color
        )
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def scatter_plot(
    variable,
    x,
    y,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    x_label = None,
    y_label = None,
    labels_font_size = 12,
    labels_font_weight = "normal",
    labels_padding = 10,
    base_color = "#00bfff",
    bubble_sizes = None,
    bubble_scale = 1.0,
    markers = "o",
    markers_size = 50,
    marker_alpha = 0.7,
    markers_edge_color = "#ffffff",
    marker_line_width = 0.5,
    show_grid = True,
    grid_axis = "both",
    grid_color = "#ffffff",
    grid_line_style = "--",
    grid_line_width = 0.5,
    grid_alpha = 0.5,
    x_ticks = None,
    y_ticks = None,
    x_tick_labels = None,
    y_tick_labels = None,
    ticks_font_size = 10,
    ticks_rotation = 0,
    x_limit = None,
    y_limit = None,
    x_margin = 0,
    y_margin = 0,
    spines_visible = (False, False, True, True),
    show_legend = False,
    legend_label = None,
    legend_location = "best",
    legend_bbox_to_anchor = None,
    legend_frame = False,
    legend_edge_color = None,
    legend_background_color = None,
    layout_padding = 2.5,
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    marker_sizes = [size * bubble_scale for size in bubble_sizes] if bubble_sizes is not None else markers_size
    scatter = axes.scatter(
        x,
        y,
        color = base_color,
        marker = markers,
        s = marker_sizes,
        alpha = marker_alpha,
        edgecolor = markers_edge_color,
        linewidths = marker_line_width,
        label = legend_label if legend_label is not None else variable
    )
    axes.set_xlabel(x_label if x_label is not None else "X", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    axes.set_ylabel(y_label if y_label is not None else "Y", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    if show_grid:
        axes.grid(
            visible = True,
            axis = grid_axis,
            color = grid_color,
            linestyle = grid_line_style,
            linewidth = grid_line_width,
            alpha = grid_alpha
        )
    if x_ticks is not None: axes.set_xticks(x_ticks)
    if y_ticks is not None: axes.set_yticks(y_ticks)
    if x_tick_labels is not None: axes.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: axes.set_yticklabels(y_tick_labels)
    axes.tick_params(axis = "both", labelsize = ticks_font_size, rotation = ticks_rotation)
    if x_limit is not None: axes.set_xlim(x_limit)
    if y_limit is not None: axes.set_ylim(y_limit)
    axes.margins(x = x_margin, y = y_margin)
    axes.spines["top"].set_visible(spines_visible[0])
    axes.spines["right"].set_visible(spines_visible[1])
    axes.spines["bottom"].set_visible(spines_visible[2])
    axes.spines["left"].set_visible(spines_visible[3])
    if show_legend:
        axes.legend(
            loc = legend_location,
            bbox_to_anchor = legend_bbox_to_anchor,
            frameon = legend_frame,
            edgecolor = legend_edge_color,
            facecolor = legend_background_color
        )
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def heat_map(
    variable,
    matrix,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    color_palette = None,
    base_color = "#00bfff",
    color_saturation_range = (0.75, 1.0),
    color_value_range = (0.25, 0.75),
    color_palette_steps = 256,
    x_label = None,
    y_label = None,
    labels_font_size = 12,
    labels_font_weight = "normal",
    labels_padding = 10,
    interpolation = "nearest",
    aspect = "equal",
    origin = "upper",
    show_colorbar = True,
    colorbar_label = None,
    x_ticks = None,
    y_ticks = None,
    x_tick_labels = None,
    y_tick_labels = None,
    ticks_font_size = 10,
    ticks_rotation = 0,
    layout_padding = 2.5,
    export_path = None,
    **kwargs,
):
    if "cmap" in kwargs: color_palette = kwargs.pop("cmap")
    if kwargs: raise TypeError(f"heat_map() got unexpected keyword argument(s): {", ".join(kwargs.keys())}")
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size)
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    axes.set_title(title, fontsize = title_font_size, fontweight = title_font_weight, pad = title_padding)
    resolved_color_palette = _resolve_color_palette(
        color_palette,
        base_color = base_color,
        color_saturation_range = color_saturation_range,
        color_value_range = color_value_range,
        colors_number = color_palette_steps,
        continuous = True
    )
    im = axes.imshow(
        matrix,
        cmap = resolved_color_palette,
        interpolation = interpolation,
        aspect = aspect,
        origin = origin
    )
    if show_colorbar:
        divider = make_axes_locatable(axes)
        cax = divider.append_axes("right", size = "5%", pad = 0.15)
        cbar = figure.colorbar(im, cax = cax)
        if colorbar_label: cax.set_ylabel(colorbar_label, rotation = 270, labelpad = 15)
    axes.set_xlabel(x_label if x_label is not None else "Columnas", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    axes.set_ylabel(y_label if y_label is not None else "Filas", fontsize = labels_font_size, fontweight = labels_font_weight, labelpad = labels_padding)
    if x_ticks is not None: axes.set_xticks(x_ticks)
    if y_ticks is not None: axes.set_yticks(y_ticks)
    if x_tick_labels is not None: axes.set_xticklabels(x_tick_labels)
    if y_tick_labels is not None: axes.set_yticklabels(y_tick_labels)
    axes.tick_params(axis = "both", labelsize = ticks_font_size, rotation = ticks_rotation)
    pyplot.tight_layout(pad = layout_padding)
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()

def radar_chart(
    variable,
    categories,
    values,
    style = "dark_background",
    tool_bar = "None",
    graph_size = (16, 9),
    graph_background_color = None,
    window_title = None,
    maximize_window = True,
    icon_path = None,
    title = None,
    title_font_size = 16,
    title_font_weight = "bold",
    title_padding = 25,
    r_margin = 0,
    base_color = "#00bfff",
    radar_line_width = 2,
    radar_line_style = "-",
    radar_marker = "o",
    radar_fill = True,
    radar_alpha = 0.25,
    ticks_font_size = 10,
    show_grid = True,
    grid_color = "#ffffff",
    grid_line_style = "--",
    grid_line_width = 0.5,
    grid_alpha = 0.5,
    layout_padding = 2.5,
    labels_rotation = True,
    labels_padding = 10,
    labels_font_size = 12,
    labels_horizontal_alignment = "automatic",
    labels_vertical_alignment = "automatic",
    export_path = None,
):
    pyplot.style.use(style)
    pyplot.rcParams["toolbar"] = tool_bar
    figure, axes = pyplot.subplots(figsize = graph_size, subplot_kw = {"projection": "polar"})
    if graph_background_color is not None: figure.set_facecolor(graph_background_color)
    manager = pyplot.get_current_fig_manager()
    window_title = window_title if window_title is not None else f"Distribución de {variable.lower()}"
    _configure_graph_window(manager, window_title, maximize_window, icon_path)
    title = title if title is not None else f"Distribución de {variable.lower()}"
    title_padding_proportion = (title_padding / 72) / figure.get_size_inches()[1]
    title_text = figure.suptitle(title, fontsize = title_font_size, fontweight = title_font_weight, y = 1, va = "top")
    title_text.set_in_layout(False)
    figure.canvas.draw()
    renderer = figure.canvas.get_renderer()
    title_height_proportion = title_text.get_window_extent(renderer = renderer).transformed(figure.transFigure.inverted()).height
    if r_margin is not None: axes.margins(y = r_margin)
    angles = numpy.linspace(0, 2 * numpy.pi, len(categories), endpoint = False).tolist()
    values = values.tolist() if hasattr(values, "tolist") else list(values)
    values += values[:1]
    angles += angles[:1]
    axes.plot(angles, values, color = base_color, linewidth = radar_line_width, linestyle = radar_line_style, marker = radar_marker)
    if radar_fill: axes.fill(angles, values, color = base_color, alpha = radar_alpha)
    axes.set_xticks(angles[:-1])
    axes.set_xticklabels([])
    axes.tick_params(axis = "y", labelsize = ticks_font_size)
    if show_grid:
        axes.grid(
            visible = True,
            color = grid_color,
            linestyle = grid_line_style,
            linewidth = grid_line_width,
            alpha = grid_alpha
        )
    pyplot.tight_layout(pad = layout_padding, rect = [0, 0.05, 1, 1 - (2 * title_padding_proportion) - title_height_proportion])
    title_text.set_y(1 - title_padding_proportion)
    maximum_r_value = axes.get_rmax()
    for angle, category in zip(angles, categories):
        angle_deg = numpy.rad2deg(angle)
        angle_deg %= 360
        horizontal_alignment = labels_horizontal_alignment
        vertical_alignment = labels_vertical_alignment
        if labels_rotation:
            rotation = angle_deg - 90 if 0 <= angle_deg <= 180 else angle_deg + 90
            horizontal_alignment = "center" if labels_horizontal_alignment == "automatic" else labels_horizontal_alignment
            vertical_alignment = "center" if labels_vertical_alignment == "automatic" else labels_vertical_alignment
        else:
            rotation = 0
            if labels_horizontal_alignment == "automatic":
                if (45 < angle_deg < 135) or (225 < angle_deg < 315): horizontal_alignment = "center"
                elif 135 <= angle_deg <= 225: horizontal_alignment = "right"
                else: horizontal_alignment = "left"
            if labels_vertical_alignment == "automatic":
                if 45 <= angle_deg <= 135: vertical_alignment = "bottom"
                elif 225 <= angle_deg <= 315: vertical_alignment = "top"
                else: vertical_alignment = "center"
        axes.text(
            angle,
            maximum_r_value + labels_padding,
            category,
            fontsize = labels_font_size,
            horizontalalignment = horizontal_alignment,
            verticalalignment = vertical_alignment,
            rotation = rotation,
            rotation_mode = "anchor"
        )
    if export_path: pyplot.savefig(export_path, bbox_inches = "tight")
    pyplot.show()