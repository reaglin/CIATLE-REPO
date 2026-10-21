using System.Text.Json;
using PreseMakerRepo.Api.Helpers;
using PreseMakerRepo.Core.Enums;
using Xunit;

namespace PreseMakerRepo.Tests;

/// <summary>
/// The "Other" allowlist in appsettings.json holds ".ext:mime" entries; the check used to compare
/// the bare content type with the whole entry, so every Other file was refused (2026-10-21).
/// </summary>
public class MaterialTypeHelperTests
{
    private static string[] ConfiguredOtherMimeTypes()
    {
        using var doc = JsonDocument.Parse(File.ReadAllText(Path.Combine(AppContext.BaseDirectory, "appsettings.json")));
        return doc.RootElement.GetProperty("Storage").GetProperty("OtherMimeTypes")
                  .EnumerateArray().Select(e => e.GetString()!).ToArray();
    }

    [Theory]
    [InlineData("text/csv", "data.csv")]
    [InlineData("application/json", "module_index.json")]
    [InlineData("image/webp", "picture.webp")]
    [InlineData("video/mp4", "clip.mp4")]
    [InlineData("TEXT/CSV", "DATA.CSV")]
    [InlineData("text/xml; charset=utf-8", "feed.xml")]
    public void Other_accepts_the_configured_types(string contentType, string fileName) =>
        Assert.True(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, contentType, ConfiguredOtherMimeTypes(), fileName));

    [Fact]
    public void Other_refuses_a_type_not_on_the_list() =>
        Assert.False(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, "application/x-msdownload", ConfiguredOtherMimeTypes(), "setup.exe"));

    [Fact]
    public void Other_accepts_octet_stream_only_for_a_listed_extension()
    {
        var list = ConfiguredOtherMimeTypes();
        Assert.True(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, "application/octet-stream", list, "font.woff2"));
        Assert.False(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, "application/octet-stream", list, "setup.exe"));
        Assert.False(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, "application/octet-stream", list, null));
    }

    [Fact]
    public void A_bare_mime_entry_still_works() =>
        Assert.True(MaterialTypeHelper.IsMimeAccepted(MaterialType.Other, "text/plain", ["text/plain"], "notes.txt"));

    [Fact]
    public void Fixed_types_ignore_parameters_and_keep_their_list()
    {
        Assert.True(MaterialTypeHelper.IsMimeAccepted(MaterialType.PrintableHTML, "text/html; charset=utf-8", [], "page.html"));
        Assert.False(MaterialTypeHelper.IsMimeAccepted(MaterialType.PrintableHTML, "text/csv", [], "data.csv"));
        Assert.True(MaterialTypeHelper.IsMimeAccepted(MaterialType.Assignment, "text/markdown", [], "assignment.md"));
    }

    [Theory]
    [InlineData(".csv:text/csv", ".csv", "text/csv")]
    [InlineData("text/plain", "", "text/plain")]
    [InlineData(".tiff", ".tiff", "")]
    public void Allowlist_entries_split_into_extension_and_type(string entry, string ext, string mime) =>
        Assert.Equal((ext, mime), MaterialTypeHelper.SplitAllowlistEntry(entry));
}
