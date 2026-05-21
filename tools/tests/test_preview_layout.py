import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PIL import Image

from deckit_dev.cli import _package_preview, _preview_column_count, _preview_output_paths


class PreviewLayoutTests(unittest.TestCase):
    def make_run(self, slide_count: int) -> Path:
        root = Path(tempfile.mkdtemp(prefix="deckit-preview-test-"))
        (root / "work").mkdir(parents=True)
        generated = root / "assets" / "generated-slides"
        generated.mkdir(parents=True)
        (root / "dist").mkdir(parents=True)

        storyboard = []
        for index in range(1, slide_count + 1):
            slide_id = f"{index:02d}_slide"
            storyboard.append(f"## {slide_id}\n- **Title**: Slide {index}\n")
            image = Image.new("RGB", (1600, 900), (index % 255, 16, 32))
            image.save(generated / f"{slide_id}.png")
        (root / "work" / "storyboard.md").write_text("\n".join(storyboard), encoding="utf-8")
        return root

    def test_preview_column_thresholds(self):
        expected = {
            1: 1,
            2: 1,
            3: 1,
            4: 2,
            8: 2,
            9: 3,
            15: 3,
            16: 4,
            32: 4,
        }
        for slide_count, cols in expected.items():
            with self.subTest(slide_count=slide_count):
                self.assertEqual(_preview_column_count(slide_count), cols)

    def test_single_preview_uses_plain_name_and_three_slides_single_column(self):
        run = self.make_run(3)
        [preview] = _package_preview(run, None, width=900, gap=24)

        self.assertEqual(preview.name, "preview.png")
        with Image.open(preview) as image:
            self.assertEqual(image.size, (900, 1566))

    def test_four_slides_use_two_by_two_grid(self):
        run = self.make_run(4)
        [preview] = _package_preview(run, None, width=900, gap=24)

        with Image.open(preview) as image:
            self.assertEqual(image.size, (900, 516))

    def test_more_than_32_slides_generates_numbered_files_only(self):
        run = self.make_run(33)
        previews = _package_preview(run, None, width=900, gap=24)

        self.assertEqual([path.name for path in previews], ["preview-01.png", "preview-02.png"])
        self.assertFalse((run / "dist" / "preview.png").exists())
        with Image.open(previews[0]) as image:
            self.assertEqual(image.size, (900, 1096))
        with Image.open(previews[1]) as image:
            self.assertEqual(image.size, (900, 506))

    def test_custom_out_path_is_used_as_numbered_base_for_multiple_chunks(self):
        run = self.make_run(65)
        previews = _package_preview(run, Path("dist/vertical-preview.png"), width=900, gap=24)

        self.assertEqual(
            [path.name for path in previews],
            ["vertical-preview-01.png", "vertical-preview-02.png", "vertical-preview-03.png"],
        )
        self.assertFalse((run / "dist" / "vertical-preview.png").exists())

    def test_preview_output_paths_scheme_a(self):
        with tempfile.TemporaryDirectory(prefix="deckit-preview-path-test-") as tmp:
            run = Path(tmp)
            self.assertEqual(
                [path.name for path in _preview_output_paths(run, Path("dist/preview.png"), 1)],
                ["preview.png"],
            )
            self.assertEqual(
                [path.name for path in _preview_output_paths(run, Path("dist/preview.png"), 2)],
                ["preview-01.png", "preview-02.png"],
            )


if __name__ == "__main__":
    unittest.main()
