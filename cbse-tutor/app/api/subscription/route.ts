import { NextRequest, NextResponse } from "next/server";

export async function POST() {
  const res = NextResponse.json({ ok: true });
  res.cookies.set("subscribed", "true", { httpOnly: false, path: "/", maxAge: 60 * 60 * 24 * 30 });
  return res;
}

export async function GET(req: NextRequest) {
  const cookie = req.cookies.get("subscribed")?.value === "true";
  return NextResponse.json({ subscribed: cookie });
}