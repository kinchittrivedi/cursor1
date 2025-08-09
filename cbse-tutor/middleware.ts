import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  if (pathname.startsWith("/tutor")) {
    const subscribed = request.cookies.get("subscribed")?.value === "true";
    if (!subscribed) {
      const url = request.nextUrl.clone();
      url.pathname = "/subscribe";
      return NextResponse.redirect(url);
    }
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/tutor"],
};