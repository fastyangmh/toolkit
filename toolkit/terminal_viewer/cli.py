# import
import argparse

import PIL
import yaml

from toolkit.terminal_viewer.src import BaseViewer, ViewerFactory


# def
def parse_args():
    parser = argparse.ArgumentParser(
        description="Terminal Viewer",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--viewer_type",
        type=str,
        choices=tuple(ViewerFactory.registry.keys()),
        default="",
        help=(
            "Type of the terminal viewer to use. "
            "If not specified, the system will try to determine the best viewer automatically."
        ),
    )
    parser.add_argument(
        "--display_kwargs",
        type=yaml.safe_load,
        default="{}",
        help="Additional keyword arguments for the viewer, in YAML format.",
    )

    parser.add_argument(
        "source",
        type=str,
        help="Source to view",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    viewers: list[BaseViewer] = []

    if args.viewer_type == "":
        for viewer_type in ViewerFactory.registry:
            viewer = ViewerFactory.build(viewer_type, {})
            viewers.append(viewer)
    else:
        viewer = ViewerFactory.build(args.viewer_type, {})
        viewers.append(viewer)

    for viewer in viewers:
        try:
            viewer.display(args.source, **args.display_kwargs)
        except (PIL.UnidentifiedImageError, ValueError):
            if args.viewer_type != "":
                print(
                    f"Viewer {viewer.__class__.__name__} could not "
                    f"handle the source: {args.source}\n"
                    "Please check the source or viewer type."
                )
        else:
            break


if __name__ == "__main__":
    main()
